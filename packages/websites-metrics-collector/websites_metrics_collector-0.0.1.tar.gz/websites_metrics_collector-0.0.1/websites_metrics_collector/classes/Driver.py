from websites_metrics_collector.communication.webpages_fetcher import fetch_list_of_urls
from confluent_kafka_producers_wrapper.producer import Producer
import logging
from typing import Optional,Tuple

logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO
)


class Driver:
    """
    This Class has one high-level method produce_metrics_for_websites to produce metrics for
    each of the url provided with the list_of_urls_to_check.
    For each successful check, it produces a message to the Kafka Topic provided as parameter
    Please note that the configuration for starting the Producer instance will be auto loaded from the ENV variables.

    """

    def __init__(self, topic: str,skip_producer_init=0):
        if not skip_producer_init:
            self._producer = Producer(topic=topic)

    async def produce_metrics_for_websites(self, list_of_urls_to_check: list,
                                           produce_message: Optional[int] = 1) ->Tuple:
        """
        This method will wait for the results from the fetch_list_of_urls function.
        For each result, if the http_status is 200 a message will be produced to Kafka
        :param list_of_urls_to_check:
        :return: bool
        """
        try:
            results = await fetch_list_of_urls(list_of_urls=list_of_urls_to_check)
            for result in results:
                if result.http_status == 200:
                    message = {
                        "url": result.url,
                        "http_status": result.http_status,
                        "elapsed_time": result.elapsed_time,
                        "pattern_verified": result.pattern_verified
                    }
                    if produce_message:
                        logger.info(f'Producing metrics for {result.url}')
                        self._producer.produce_message(value=message, key={"service_name": "name"})
            return results
        except Exception as error:
            logger.error(f"An EXCEPTION {error} occurred")
