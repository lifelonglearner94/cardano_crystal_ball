default:
	pytest

clean:
	clean_pythonstuff clean_notbookstuff

clean_pythonstuff:
	find . | grep -E "(__pycache__|\.pyc$|\.pytest_cache)" | xargs rm -rvf

clean_notbookstuff:
	find . | grep -E "(\.ipynb_checkpoints)" | xargs rm -rvf

pylint:
	find . -iname "*.py" -not -path "./tests/*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

pytest:
  PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

run_api:
	uvicorn cardano_crystal_ball.api.fast:app --reload

make_preprocessor:
	python cardano_crystal_ball/interface/main.py

run_training:
	python -c 'from cardano_crystal_ball.interface.main import training; training()'

run_init_model:
	python -c 'from cardano_crystal_ball.ml_logic.model import initialize_and_compile_model; initialize_and_compile_model()'

streamlit:
	-@streamlit run cardano_crystal_ball_website/app.py

gar_creation:
	gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev
	gcloud artifacts repositories create ${GAR_REPO} --repository-format=docker \
	--location=${GCP_REGION} --description="Repository for storing ${GAR_REPO} images"

docker_build:
	docker build --platform linux/amd64 -t ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod .

docker_push:
	docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod

docker_run:
	docker run -e PORT=8000 -p 8000:8000 --env-file .env ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod

docker_interactive:
	docker run -it --env-file .env ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod /bin/bash

docker_deploy:
	gcloud run deploy --image ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${GAR_REPO}/${GAR_IMAGE}:prod --memory ${GAR_MEMORY} --region ${GCP_REGION}
