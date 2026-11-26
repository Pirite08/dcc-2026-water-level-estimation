# Colab 코드와 저장된 실행 기록

처음에는 [결과 그래프를 만드는 CPU 예제](00_read_results.ipynb)를 열어 보세요. 원 데이터를 준비하지 않아도 보고서의 수치와 그래프를 확인할 수 있습니다. 당시 연구 코드는 아래 표에서 관심 있는 작업을 골라 읽고, 직접 실행하려면 [Colab 준비 안내](../docs/colab-guide.md)를 함께 확인해 주세요.

원본 Colab 노트북 11개를 읽기 쉬운 파일명으로 옮겼습니다. 각 파일 첫 셀에 목적, 입력·출력, 실제 저장된 실행 상태를 적었습니다. 원래 코드와 숫자·표·오류 등 텍스트 출력은 보존하고, 원천 데이터 사진이 섞일 수 있는 이미지 출력과 HTML·JavaScript·binary payload는 제거했습니다. 이 공개 작업에서 모델을 다시 학습하거나 test 예측·성능을 다시 계산하지 않았습니다.

원본 11개, 출력 없는 복구 코드 1개, 보고서 수치를 다시 그리는 CPU 노트북 1개를 구분해 읽어 주세요. 원래 11개와 복구 코드의 모든 code cell은 `execution_count: null`로 저장되어 있었지만, 원본 11개에는 텍스트 실행 출력이 남아 있습니다. `null`만 보고 전부 미실행이라고 판단하지 않았습니다.

원본 이름과 원본·공개본 SHA-256은 [대응표](../docs/notebook-source-map.csv)에 기록했습니다. 원본 파일의 hash와 공개본의 hash가 다른 것은 소개 셀 추가, 비공개 식별자 치환, metadata와 이미지 출력 제거 때문입니다. CPU 결과 읽기 노트북은 새로 작성한 별도 파일이므로 이 원본 대응표에 포함하지 않습니다.

| 읽어 볼 코드 | 하는 일 | 남아 있는 실행 기록 | Colab |
|---|---|---|---|
| [환경과 파일 읽기 점검](00_environment_smoke.ipynb) | 작은 자료 묶음으로 환경과 압축 파일 확인 | GPU·ZIP 검사는 통과했으나, 잘린 JPEG 1개를 읽는 과정에서 중단 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/00_environment_smoke.ipynb) |
| [전체 데이터의 품질 점검](01_data_audit.ipynb) | 이미지와 정답의 대응, 저장 형식과 손상 검사 | 22개 묶음을 검사했고, 형식 불일치 153개로 최종 완료 검사를 통과하지 못한 기록 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/01_data_audit.ipynb) |
| [분포 살펴보기와 학습·평가 자료 분할](02_eda_and_split.ipynb) | 같은 이미지 그룹을 함께 두는 8:1:1 분할과 시각화 | 후속 보정 결과를 읽어 예외 자료를 분리한 뒤 분할 완료. 앞 단계의 보정 코드 01R은 미확보 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/02_eda_and_split.ipynb) |
| [반복 학습용 입력 자료 만들기](03a_dataset_preparation.ipynb) | 학습 자료 묶음과 익명 테스트 입력 준비 | 전체 자료 실행으로 학습 246,308장 / 검증 30,808장 / 테스트 30,809장 준비 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/03a_dataset_preparation.ipynb) |
| [세 모델 비교와 선택 모델의 전체 학습](03b_backbone_comparison.ipynb) | 세 CNN 후보 비교와 전체 사진 기반 수위 학습 | 현재 출력은 ConvNeXt-Tiny 5에폭 전체 학습, 검증 RMSE 0.264505 m. 초기 세 후보 비교 수치는 보고서에 기록 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/03b_backbone_comparison.ipynb) |
| [작은 목자판을 찾아 확대해서 예측하기](03c_roi_regression.ipynb) | YOLO26s로 검출한 영역을 확대해 수위 예측 | 일부 자료로 비교한 실행에서 검출 영역 기반 검증 RMSE 0.331435 m. 정답 박스를 사용한 별도 진단값은 0.228441 m | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/03c_roi_regression.ipynb) |
| [검증 결과로 모델과 처리 경로 정하기](03d_model_selection.ipynb) | 유형별로 전체 사진과 확대 입력의 경로 선택 | 전체 학습 모델을 선택한 기록, 결합 경로의 검증 RMSE 0.214397 m | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/03d_model_selection.ipynb) |
| [정답을 입력하지 않고 테스트 예측 저장하기](03e_test_prediction.ipynb) | 익명 테스트 사진을 예측하고 결과 고정 | 30,809장 입력 검사를 통과했고, 정답 접근 없이 예측 저장 완료 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/03e_test_prediction.ipynb) |
| [장애물 분포를 고려해 학습 자료 다시 나누기](04a_obstacle_rebalance.ipynb) | 테스트를 유지하고 학습·검증의 조건 분포 조정 | 실자료에서 교환 2,736회, 분포 차이 점수 20.466860→8.074058. 앞에 출력된 9회는 합성 자료로 한 자체 검사 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/04a_obstacle_rebalance.ipynb) |
| [장애물을 함께 학습하는 방법 비교하기](04b_multitask_training.ipynb) | 수위 단독 학습과 장애물 보조 학습 비교 | 수위 단독 학습 결과를 재사용하고 보조 학습을 재개해 6에폭까지 실행, 검증 기준으로 모델 선택 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/04b_multitask_training.ipynb) |
| [최종 예측의 성능과 오류 분석하기](04c_final_evaluation.ipynb) | 예측 저장 후 별도 평가 실행에서 정답과 비교 | 내부 고정 테스트 RMSE **0.142334 m** 기록. 초기 오류 분석에 사용한 테스트로 후속 비교한 결과 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/04c_final_evaluation.ipynb) |

| 별도 파일 | 용도와 실행 상태 | Colab |
|---|---|---|
| [결과 그래프 직접 만들어 보기](00_read_results.ipynb) | 새로 작성한 CPU용 결과 읽기·그림 재생성. 보고서에 기록된 수치만 사용하며 테스트 예측을 재계산하지 않음 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/00_read_results.ipynb) |
| [초기 모델의 평가 코드 복구본](historical/03f_private_evaluation_recovered.ipynb) | 초기 예측 뒤 별도로 정답과 결합해 평가하도록 작성된 코드. 저장 출력 0개이며 실행과 결과는 검증되지 않음 | [열기](https://colab.research.google.com/github/Pirite08/dcc-2026-water-level-estimation/blob/main/notebooks/historical/03f_private_evaluation_recovered.ipynb) |

## 코드에서 만나는 용어

**Manifest**는 이미지별 위치·정답·점검 결과를 정리한 관리 목록입니다. **shard**는 반복해서 읽기 좋게 묶은 학습 자료이고, **seal**은 파일의 버전·크기·검사값을 남긴 완료 기록입니다. **ROI**는 사진에서 목자판이 있는 관심영역을 뜻합니다. 아래의 내부 실행 이름은 당시 코드와 기록을 찾아보기 위해 남겼습니다.

<details>
<summary>실험 모드와 파일 연결을 자세히 확인하기</summary>

### 실행 관계와 끊어진 연결

번호순으로 한 번 실행하면 모두 재현되는 묶음은 아닙니다. 여러 실행 모드와 별도 세션에서 저장한 파일들이며, 각 단계는 상위 seal의 generation·크기·SHA-256·schema·config를 확인합니다. 현재 저장된 출력이 어느 모드의 기록인지는 위 표와 각 소개 셀을 기준으로 읽으세요.

```text
00 환경 점검 → 01 전수 감사 [현재 저장 기록: 최종 gate 실패]
                    ↓
             01R 복구·승인된 v2 seal [코드 누락]
                    ↓
               02 EDA·v3 split
                    ↓
               03A dataset 준비
                    ↓
       03B pilot_compare → 03C pilot_candidate → 03D pilot_select
                                             ↓
       03B full_retrain → 03C full_retrain → 03D full_promote
                                             ↓
                                      03E 익명 예측 봉인
                                             ↓
                                      03F private 평가
                                      [복구 코드만, 출력 없음]

02의 고정 test + 03A의 full shard
                    ↓
          04A train/val 재분할·v4 dataset
                    ↓
          04B 고정 router·두 학습 arm·선택 봉인
                    ↓
          04C INFERENCE [새 GPU runtime]
                    ↓
          04C EVALUATION [새 CPU runtime, 예측 검증 후 truth 접근]
```

03B의 현재 저장 기록은 full 재학습이고 03C의 현재 기록은 pilot입니다. 03D의 현재 full 승격 출력을 이 두 파일의 현재 출력만으로 모두 검증할 수는 없습니다. 03A도 `m3ds-v2-pilot`이라는 version 이름과 `full` profile이 함께 기록되어 있으므로 이름만으로 pilot 실행이라고 분류하지 않았습니다. 복구된 03F는 누락된 01R을 채우지 않습니다.

04A 이후에도 기존 test 30,809개를 유지합니다. 04C 코드와 출력의 평가 범위는 `internal_fixed_holdout_after_prior_truth_exposure`입니다. 보고된 0.142334 m는 이전 실험에서 정답을 확인한 내부 고정 holdout의 후속 결과이며, 외부 공식 평가나 새로운 미관측 test 검증을 뜻하지 않습니다.

</details>

## 직접 실행하려면

1. 원천 데이터에 대한 사용 권한과 원천·라벨 ZIP, 필요한 상위 Manifest·seal·shard·모델 가중치를 별도로 준비합니다. 공개 저장소에는 원천 사진, private test 연결표와 정답, 가중치, 원래 GCS 객체를 배포하지 않습니다.
2. 코드의 `YOUR_GCP_PROJECT_ID`와 `YOUR_GCS_BUCKET`을 본인 설정으로 바꾸고 Colab에서 해당 계정으로 인증합니다. `YOUR_ACCOUNT@example.invalid`는 가려진 과거 출력이고 인증 정보가 아닙니다. `YOUR_LOCAL_DATA_ROOT`는 업로드 안내의 로컬 데이터 폴더 예시입니다.
3. 단계별 설정과 상위 산출물의 계보를 확인합니다. 01R과 일부 중간 실행 산출물이 없으므로 현재 공개본만으로 전체 경로를 재현할 수 없습니다. 보존된 SHA-256·generation·config gate를 건너뛰어 과거 결과를 재현했다고 주장하지 마세요.
4. GPU 학습·추론 파일과 CPU 준비·평가 파일의 runtime 요구를 원래 안내에서 확인합니다. 03C는 새 GPU runtime을, 04C는 추론과 평가를 나눈 두 runtime을 요구합니다. 이 공개 작업에서는 해당 실행을 수행하지 않았습니다.

데이터 없이 결과의 흐름을 먼저 보려면 [CPU 결과 읽기 노트북](00_read_results.ipynb)을 여세요. 이 노트북의 그림 재생성은 보고서 수치의 시각화이며, 원래 raw prediction으로 RMSE를 다시 계산한 검증과는 구분합니다.

## 공개본에서 바꾼 내용

- 원본 code cell 122개를 순서대로 보존했습니다. 계산·모델·학습·HMAC 생성·hash 검증 코드를 새 구현으로 교체하지 않았으며, 원래 개인 GCP 프로젝트·버킷 식별자만 일관된 placeholder로 치환했습니다. 계정 이메일과 개인 로컬 데이터 경로도 가렸습니다.
- 저장된 숫자, 일반 텍스트 표, 로그, 오류 출력은 남겼습니다. 8개 PNG payload, 15개 HTML payload와 15개 Colab rich-display payload를 제거하고 Markdown 출력 1개는 일반 텍스트로 바꿨습니다. 공개 display MIME은 text/plain만 남겼습니다. 원본 데이터 사진을 이 저장소에서 볼 수 없도록 했으며 그림 셀의 코드 자체는 남아 있습니다.
- Colab Drive ID, 작성자·widget·출력 ID 등 비공개 metadata를 제거하고 nbformat과 kernelspec/language 정보는 보존했습니다. 첫 셀의 한국어 안내, 코드/Colab 링크와 원본 대응표를 추가했습니다.
- 원래 문서의 “완료 기준”, 다음 단계, 예상 실행량은 작성 당시의 안내입니다. 실제 저장 실행 상태는 공개 소개 셀에 별도로 적었습니다. 누락된 실행을 새로 실행한 것처럼 채우지 않았습니다.
