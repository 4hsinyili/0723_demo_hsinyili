lambdas-pre-deploy:
	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/.env QS_Lambdas/qs_log_result/src/QS_Modules/.env QS_Lambdas/qs_track_topic/src/QS_Modules/.env < QS_Modules/.env >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/env.py QS_Lambdas/qs_log_result/src/QS_Modules/env.py QS_Lambdas/qs_track_topic/src/QS_Modules/env.py < QS_Modules/env.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/utils.py QS_Lambdas/qs_log_result/src/QS_Modules/utils.py QS_Lambdas/qs_track_topic/src/QS_Modules/utils.py < QS_Modules/utils.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Modules/models.py QS_Lambdas/qs_log_result/src/QS_Modules/models.py QS_Lambdas/qs_track_topic/src/QS_Modules/models.py < QS_Modules/models.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Crawlers/crawl_detail.py QS_Lambdas/qs_log_result/src/QS_Crawlers/crawl_detail.py QS_Lambdas/qs_track_topic/src/QS_Crawlers/crawl_detail.py < QS_Crawlers/crawl_detail.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Crawlers/crawl_list.py QS_Lambdas/qs_log_result/src/QS_Crawlers/crawl_list.py QS_Lambdas/qs_track_topic/src/QS_Crawlers/crawl_list.py < QS_Crawlers/crawl_list.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/src/QS_Crawlers/lambda_modules.py QS_Lambdas/qs_log_result/src/QS_Crawlers/lambda_modules.py QS_Lambdas/qs_track_topic/src/QS_Crawlers/lambda_modules.py < QS_Crawlers/lambda_modules.py >/dev/null

	tee QS_Lambdas/qs_crawl_topic/bin/chromedriver QS_Lambdas/qs_track_topic/bin/chromedriver < QS_Crawlers/chromedriver >/dev/null

build-all-lambdas-package:
	cd QS_Lambdas/qs_crawl_topic && $(MAKE) build-lambda-package
	cd QS_Lambdas/qs_log_result && $(MAKE) build-lambda-package
	cd QS_Lambdas/qs_track_topic && $(MAKE) build-lambda-package
