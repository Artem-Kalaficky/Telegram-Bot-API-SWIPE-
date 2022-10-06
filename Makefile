extract:
	pybabel extract --input-dirs=. -o locales/API_SWIPE.pot

update:
	pybabel update -d locales -D API_SWIPE -i locales/API_SWIPE.pot

init:
	pybabel init -i locales/API_SWIPE.pot -d locales -D API_SWIPE -l uk

compile:
	pybabel compile -d locales -D API_SWIPE

run:
	pybabel compile -d locales -D API_SWIPE
	python bot.py