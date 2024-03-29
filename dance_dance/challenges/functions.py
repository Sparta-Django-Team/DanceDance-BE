import logging
import os
import time
from datetime import datetime

import cv2
import librosa
import mediapipe as mp
import moviepy.editor as mvp
import numpy as np
import pandas as pd
from pytube import YouTube
from sklearn.metrics.pairwise import cosine_similarity

from dance_dance.challenges.models import OriginalVideoTag, Tag

logger = logging.getLogger("django")


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        logger.info("Error: Creating directory. " + directory)


def match_sync(vpath_1, vpath_2):
    # 비디오 파일 로드
    video1 = mvp.VideoFileClip(vpath_1)
    video2 = mvp.VideoFileClip(vpath_2)

    # Audio 파일 경로 설정
    mp3_file1 = "./temp/audios/audio_1.mp3"
    mp3_file2 = "./temp/audios/audio_2.mp3"

    create_folder("./temp/audios/")

    # Audio 파일 생성
    logger.info("Creating Audio files...")
    video1.audio.write_audiofile(mp3_file1)
    video2.audio.write_audiofile(mp3_file2)

    # Audio 파일 load
    logger.info("Loading audio files...")
    y1, sr1 = librosa.load(mp3_file1, offset=5, duration=10)
    y2, sr2 = librosa.load(mp3_file2, offset=5, duration=10)

    # cross-correlation 계산
    logger.info("Calculating Cross-Correlation...")
    correlation = np.correlate(y1, y2, mode="full")
    peak_index = np.argmax(correlation)  # peak index (correlation이 가장 큰 지점의 인덱스)

    # sync 차이 계산 (peak 위치를 초 단위로 변환)
    sync_difference_seconds = round((peak_index - len(y2) + 1) / sr1 * 10, 0)
    logger.info(f"Sync difference: 약 {sync_difference_seconds:.2f} * 0.1 sec")
    return sync_difference_seconds


def get_landmarks(video_route, file_type):
    create_folder("./temp/landmarks/origin/")
    create_folder("./temp/landmarks/user/")

    # clm_list 생성
    clm_list = ["idx"]
    coordinates = ["x", "y", "z"]
    sides = ["l", "r"]
    for body_part in ["shld", "elbw", "wrst", "hip", "knee", "ankl"]:
        for side in sides:
            for coordinate in coordinates:
                clm_list.append(f"{side}_{body_part}_{coordinate}")

    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    pose = mp_pose.Pose()

    cap = cv2.VideoCapture(video_route)
    title = os.path.splitext(os.path.basename(video_route))[0]

    # 새로운 비디오 생성을 위한 설정
    output_directory = f"./temp/videos/output/{file_type}/"
    os.makedirs(output_directory, exist_ok=True)

    output_video_path = f"./temp/videos/output/{file_type}/{title}_landmarks.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"DIVX")
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    logger.info("fps:" + str(fps))
    frame_size = (int(cap.get(3)), int(cap.get(4)))  # 원본 동영상의 크기로 프레임 크기 설정

    # 비디오 저장기 초기화
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)
    df = pd.DataFrame(columns=clm_list)  # 빈 dataframe 생성

    # 랜드마크 추출 인터벌 설정
    extract_interval_seconds = 0.1
    extract_interval_frames = fps * extract_interval_seconds  # 0.1초마다 생성되는 프레임 수 (float : 2.997002997002997)

    frame_count = 0
    sec = 0.0
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        logger.info("Extracting landmarks...")
        # while True:
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break
            progress_percentage = round(sec / (length / fps) * 10, 0)
            print("\r진행률: {}%".format(progress_percentage), end="", flush=True)
            frame_count += 1
            if frame_count // extract_interval_frames >= sec:
                sec = round(sec + 1, 1)

                img = cv2.resize(img, (200, 400))
                results = pose.process(img)
                x = [sec]
                # 랜드마크 생성
                if results.pose_landmarks:
                    mp_draw.draw_landmarks(
                        img,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                    )
                    for k in range(33):
                        if (11 <= k < 17) or (23 <= k < 29):
                            x.append(round(results.pose_landmarks.landmark[k].x, 3))
                            x.append(round(results.pose_landmarks.landmark[k].y, 3))
                            x.append(round(results.pose_landmarks.landmark[k].z, 3))
                            # x.append(results.pose_landmarks.landmark[k].visibility)
                else:
                    for k in range(36):
                        x.append(0.000)
                tmp = pd.DataFrame([x], columns=clm_list)
                df = pd.concat([df, tmp])
                # 랜드마크가 표시된 프레임을 저장
                out.write(img)
                cv2.imshow("Estimation", img)
                cv2.waitKey(1)

    # 비디오 저장기 닫기
    cap.release()
    out.release()

    cv2.destroyAllWindows()

    csv_path = f"./temp/landmarks/{file_type}/{title}.csv"
    df.to_csv(csv_path, index=False)
    logger.info("Complete creating landmarks...")
    return [output_video_path, csv_path]


class GetScores:
    def __init__(self):
        self.now = datetime.now()

    @staticmethod
    def compare_videos(lpath_1, lpath_2, sync_difference_seconds):
        diff = int(sync_difference_seconds)

        # load data
        data1 = pd.read_csv(lpath_1)
        data2 = pd.read_csv(lpath_2)

        if diff > 0:
            ldmk_1 = np.array(data1)[1 + diff :, 1:]
            ldmk_2 = np.array(data2)[1:, 1:]
        elif diff == 0:
            ldmk_1 = np.array(data1)[1:, 1:]
            ldmk_2 = np.array(data2)[1:, 1:]
        else:
            ldmk_1 = np.array(data1)[1:, 1:]
            ldmk_2 = np.array(data2)[1 + (diff * (-1) + 1) :, 1:]

        r1, c1 = ldmk_1.shape
        r2, c2 = ldmk_2.shape
        logger.info(f"r1, c1: {r1}, {c1}\nr2, c2: {r2}, {c2}")

        length_val = min(r1, r2)
        logger.info(f"length of landmarks: {length_val}")
        ldmk_1 = ldmk_1[:length_val]
        ldmk_2 = ldmk_2[:length_val]

        cosine_sim = cosine_similarity(ldmk_1, ldmk_2)
        results = np.round_(np.diag(cosine_sim), 2).tolist()
        logger.info("-----Results of Cosine Similarity-----")
        logger.info(results)
        mean_score = np.mean(results)
        logger.info(f"score: {str(round(mean_score*100, 1))}점")

        return [mean_score, results]


# 영상 업로드, 랜드마크
def download_video(video_url, file_type):
    start_time = time.time()
    now = datetime.now()
    DOWNLOAD_DIR = f"./temp/videos/{file_type}"
    yt = YouTube(video_url)

    # 유튜브 영상 정보 추출
    channel_name = yt.author
    thumbnail_image_url = yt.thumbnail_url
    uploaded_date = yt.publish_date
    hits = yt.views

    # 영상 제목에서 키워드(#해시태그) 추출
    keywords = [x.strip().lower() for x in yt.title.split("#")][1:]
    logger.info(keywords)
    for keyword in keywords:
        if Tag.objects.filter(name=keyword):
            chl_name = keyword
            chl_tag = Tag.objects.get(name=keyword)
            logger.info(chl_tag.parent_tag_id)
            break
        else:
            continue
    if chl_name == None:
        logger.info("--------------챌린지를 찾을 수 없습니다.--------------")  # 직접 입력하도록 UI 구현 필요

    # 영상 제목 설정 후 지정된 경로에 저장
    video_title = (str(now.strftime("%Y%m%d%H%M")) + "_" + str(chl_tag.parent_tag_id) + "_" + str(channel_name)).replace(" ", "")
    yt.streams.filter(res="360p", file_extension="mp4").first().download(output_path=DOWNLOAD_DIR, filename=f"{video_title}.mp4")
    video_file_path = f"./temp/videos/{file_type}/{video_title}.mp4"

    # 결과 데이터 results의 각 인자로 저장
    results = {
        "title": video_title,
        "youtube_video_url": video_url,
        "channel_name": channel_name,
        "thumbnail_image_url": thumbnail_image_url,
        "uploaded_at": uploaded_date,
        "challenge_name": chl_name,
        "tags": ",".join(str(s) for s in keywords),
        "platform_type_id": 1,  # 1: Youtube
    }
    if file_type == "user":
        origin_video_tag = OriginalVideoTag.objects.select_related("original_video_id").get(tag_id=chl_tag.parent_tag_id)
        origin_video = origin_video_tag.original_video_id
        sync_difference_seconds = match_sync(origin_video.video_file_path, video_file_path)
        outputs = get_landmarks(video_file_path, file_type)  # 영상 랜드마크 추출 : output_video_path, csv_path
        motion_data_path = outputs[1]  # 영상 랜드마크 csv 파일 저장 경로 변수 지정
        score_results = GetScores.compare_videos(
            origin_video.motion_data_path, motion_data_path, sync_difference_seconds
        )  # mean_score, results, landmarks
        results["score"] = score_results[0]
        results["score_list"] = ",".join(map(str, score_results[1]))
        # results['is_rank] = rank 확인 함수 생성 후 추가
    elif file_type == "origin":
        outputs = get_landmarks(video_file_path, file_type)  # 영상 랜드마크 추출 : output_video_path, csv_path
        motion_data_path = outputs[1]  # 영상 랜드마크 csv 파일 저장 경로 변수 지정
        results["hits"] = hits
        results["video_file_path"] = video_file_path
        results["motion_data_path"] = motion_data_path
        results["platform_type_id"] = 1  # 현재 유튜브 영상(1번)만 Test 중
        # Origin Video Tag도 해당 영상에 맞도록 자동으로 추가하는 로직 필요

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Elapsed time: {elapsed_time:.1f} seconds")
    return results
