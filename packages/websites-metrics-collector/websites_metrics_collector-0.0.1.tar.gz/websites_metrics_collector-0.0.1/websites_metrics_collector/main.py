from aiohttp import web
from websites_metrics_collector.classes.Driver import Driver
import json, asyncio, os, logging

logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO
)

driver = Driver(topic=os.environ.get('topic_for_producing_metrics', 'websites_metrics'), skip_producer_init=os.environ.get('skip_producer_init', 0))


async def process_websites_to_fetch(request):
    """
    This function processes the POST request and create an asyncio task calling the Driver()'s produce_metrics_for_websites method
    passing the provided list.

    :param request:
    :return: JSON
    """
    try:
        data = await request.json()
        produce_message = os.environ.get('produce_message',1)
        if len(data) == 0:
            example_list = [["http://cloudbased.me", ["Microservices", "Antonio"]],
                            ["http://ferrari.com", ["ferrari", "italia"]], ["http://motoguzzi.com", ["italia"]]]
            error_message = {
                "message": "Bad format! You need to send me a list of URLS [['http://urltofetch.com'],['optional 1st pattern to verify in the html','optional 2nd pattern to verify in the html',''optional Nth pattern to verify in the html']]. See the example.",
                "example": example_list}
            return web.json_response(error_message, status=400, content_type='application/json', dumps=json.dumps)
        else:
            asyncio.create_task(driver.produce_metrics_for_websites(
                list_of_urls_to_check=data,produce_message=produce_message))
            return web.json_response({"urls": data, "submitted": True}, status=201, content_type='application/json',
                                     dumps=json.dumps)
    except Exception as error:
        logger.error(f"An Error {error} occurred")
        unexpected_error = f"An Error occurred and the request or the payload cannot be processed. =..= No squealing, remember that it's all in your head =..="
        return web.json_response({"message": unexpected_error}, status=403, content_type='application/json',
                                 dumps=json.dumps)

def start():
    app = web.Application()
    app.router.add_post('/api/v1/websites_metrics', process_websites_to_fetch)
    web.run_app(app, host=os.environ.get('SERVICE_HOST', '127.0.0.1'),
                port=int(os.environ.get('SERVICE_LISTEN_PORT', '8080')))


if __name__ == "__main__":
    start()