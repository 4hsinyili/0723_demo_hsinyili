lambdas-pre-deploy:
	mkdir -p QS_Lambdas/qs_crawl_topic/lib

	mkdir -p QS_Lambdas/qs_track_topic/lib

	mkdir -p QS_Lambdas/qs_log_result/lib

	mkdir -p QS_Lambdas/qs_crawl_topic/bin

	mkdir -p QS_Lambdas/qs_track_topic/bin

	mkdir -p QS_Lambdas/qs_log_result/bin

	mkdir -p QS_Lambdas/qs_crawl_topic/src/QS_Modules

	mkdir -p QS_Lambdas/qs_track_topic/src/QS_Modules

	mkdir -p QS_Lambdas/qs_log_result/src/QS_Modules

	mkdir -p QS_Lambdas/qs_crawl_topic/src/QS_Crawlers

	mkdir -p QS_Lambdas/qs_track_topic/src/QS_Crawlers

	mkdir -p QS_Lambdas/qs_log_result/src/QS_Crawlers

	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/.env QS_Lambdas/qs_log_result/src/QS_Modules/.env QS_Lambdas/qs_track_topic/src/QS_Modules/.env < QS_Modules/.env >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/env.py QS_Lambdas/qs_log_result/src/QS_Modules/env.py QS_Lambdas/qs_track_topic/src/QS_Modules/env.py < QS_Modules/env.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/utils.py QS_Lambdas/qs_log_result/src/QS_Modules/utils.py QS_Lambdas/qs_track_topic/src/QS_Modules/utils.py < QS_Modules/utils.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/models.py QS_Lambdas/qs_log_result/src/QS_Modules/models.py QS_Lambdas/qs_track_topic/src/QS_Modules/models.py < QS_Modules/models.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Crawlers/crawl_detail.py QS_Lambdas/qs_log_result/src/QS_Crawlers/crawl_detail.py QS_Lambdas/qs_track_topic/src/QS_Crawlers/crawl_detail.py < QS_Crawlers/crawl_detail.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Crawlers/crawl_list.py QS_Lambdas/qs_log_result/src/QS_Crawlers/crawl_list.py QS_Lambdas/qs_track_topic/src/QS_Crawlers/crawl_list.py < QS_Crawlers/crawl_list.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Crawlers/prod.py QS_Lambdas/qs_log_result/src/QS_Crawlers/prod.py QS_Lambdas/qs_track_topic/src/QS_Crawlers/prod.py < QS_Crawlers/prod.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/docker-compose.yml QS_Lambdas/qs_log_result/docker-compose.yml QS_Lambdas/qs_track_topic/docker-compose.yml < QS_Lambdas/docker-compose.yml >/dev/null

	tee QS_Lambdas/qs_crawl_topic/requirements.txt QS_Lambdas/qs_log_result/requirements.txt QS_Lambdas/qs_track_topic/requirements.txt < QS_Lambdas/requirements.txt >/dev/null

	cp QS_Lambdas/Dockerfile QS_Lambdas/qs_crawl_topic/
	cp QS_Lambdas/Dockerfile QS_Lambdas/qs_log_result/
	cp QS_Lambdas/Dockerfile QS_Lambdas/qs_track_topic/

	cp QS_Lambdas/Makefile QS_Lambdas/qs_crawl_topic/
	cp QS_Lambdas/Makefile QS_Lambdas/qs_log_result/
	cp QS_Lambdas/Makefile QS_Lambdas/qs_track_topic/


build-all-lambdas-package:
	cd QS_Lambdas/qs_crawl_topic && $(MAKE) build-lambda-package
	cd QS_Lambdas/qs_log_result && $(MAKE) build-lambda-package
	cd QS_Lambdas/qs_track_topic && $(MAKE) build-lambda-package

cloud-run-pre-deploy:
	tee QS_Cloud_Run/qs_crawl_topic/.env QS_Cloud_Run/qs_track_topic/.env < QS_Modules/.env >/dev/null

	tee QS_Cloud_Run/qs_crawl_topic/env.py QS_Cloud_Run/qs_track_topic/env.py < QS_Modules/env.py >/dev/null

	tee QS_Cloud_Run/qs_crawl_topic/utils.py QS_Cloud_Run/qs_track_topic/utils.py < QS_Modules/utils.py >/dev/null

	tee QS_Cloud_Run/qs_crawl_topic/models.py QS_Cloud_Run/qs_track_topic/models.py < QS_Modules/models.py >/dev/null

test-cloud-run-package:
	docker build -t qscrawltopic .
	docker run --rm -p 8080:8080 -e PORT=8080 qscrawltopic

	docker build -t qstracktopic .
	docker run --rm -p 8080:8080 -e PORT=8080 qstracktopic
# http://localhost:8080?pwd=ihatecloudflare&offset=0&limit=9&sleep=0&triggered_at_str=2021-07-15-08:25:19

	docker build -t qscloudruniptest .
	docker run --rm -p 8080:8080 -e PORT=8080 qscloudruniptest

submit-cloud-run-package:
	gcloud builds submit --tag gcr.io/qsearchcrawl/qscrawltopic
	gcloud beta run deploy qscrawltopic --image gcr.io/qsearchcrawl/qscrawltopic --region asia-east1 --platform managed

	gcloud builds submit --tag gcr.io/qsearchcrawl/qstracktopic
	gcloud beta run deploy qstracktopic --image gcr.io/qsearchcrawl/qstracktopic --region asia-east1 --platform managed

	gcloud builds submit --tag gcr.io/qsearchcrawl/qscloudruniptest
	gcloud beta run deploy qscloudruniptest --image gcr.io/qsearchcrawl/qscloudruniptest --region asia-east1 --platform managed