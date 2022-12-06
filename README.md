## So1s Model Templates

모델 컨테이너라이즈를 위한 보일러플레이트 템플릿입니다.
Dockerfile, BentoML 관련 코드 연동이 완료되면 가중치 파일을 포함한 프로젝트를 tar | zip 포맷으로 압축하신 뒤, [Web UI](https://github.com/so1s/so1s-frontend) 기반 패키지 업로드를 통해 클러스터 내부에서 빌드 및 업로드, 서빙이 가능합니다.

## 지원 사양
- [Basic CPU Template](https://github.com/so1s/so1s-model-templates/tree/cpu)
- [Basic GPU Template](https://github.com/so1s/so1s-model-templates/tree/gpu)
- [Tensorflow Template](https://github.com/so1s/so1s-model-templates/tree/tensorflow)

그 외에도 코드 수정을 통한 자유로운 바인딩이 가능합니다.

## 사용 방법

[ghcr Image](https://github.com/so1s/so1s-model-templates/pkgs/container/model-templates)로 배포되어 있어 Base Image로 사용하시는 것이 가능합니다.

Repo Clone을 통한 보일러플레이트를 ML 프로젝트에 연동하셔서 사용하시는 것도 가능합니다.
