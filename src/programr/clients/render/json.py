from programr.utils.logging.ylogger import YLogger

from programr.clients.render.renderer import RichMediaRenderer


class JSONRenderer(RichMediaRenderer):

    def __init__(self, callback=None):
        RichMediaRenderer.__init__(self, callback)

    def handle_text(self, client_context, text):
        if self._client:
            return self._client.process_response(client_context, text)
        return text

    def handle_url_button(self, client_context, button):
        if self._client:
            self._client.process_response(client_context, button)
        return button

    def handle_postback_button(self, client_context, button):
        if self._client:
            self._client.process_response(client_context, button)
        return button

    def handle_link(self, client_context, link):
        if self._client:
            self._client.process_response(client_context, link)
        return link

    def handle_image(self, client_context, image):
        if self._client:
            self._client.process_response(client_context, image)
        return image

    def handle_video(self, client_context, video):
        if self._client:
            self._client.process_response(client_context, video)
        return video

    def handle_card(self, client_context, card):
        if self._client:
            self._client.process_response(client_context, card)
        return card

    def handle_carousel(self, client_context, carousel):
        if self._client:
            self._client.process_response(client_context, carousel)
        return carousel

    def handle_reply(self, client_context, reply):
        if self._client:
            self._client.process_response(client_context, reply)
        return reply

    def handle_delay(self, client_context, delay):
        if self._client:
            self._client.process_response(client_context, delay)
        return delay

    def handle_split(self, client_context, split):
        if self._client:
            self._client.process_response(client_context, split)
        return split

    def handle_list(self, client_context, list):
        if self._client:
            self._client.process_response(client_context, list)
        return list

    def handle_ordered_list(self, client_context, list):
        if self._client:
            self._client.process_response(client_context, list)
        return list

    def handle_location(self, client_context, location):
        if self._client:
            self._client.process_response(client_context, location)
        return location
