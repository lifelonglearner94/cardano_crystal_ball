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
