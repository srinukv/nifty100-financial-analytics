load:
	python src/etl/loader.py

validate:
	python src/etl/validator.py

ratios:
	python src/ratios/ratio_engine.py

test:
	pytest

dashboard:
	streamlit run src/dashboard/app.py

report:
	python src/reports/report_generator.py

clean:
	del /Q *.pyc