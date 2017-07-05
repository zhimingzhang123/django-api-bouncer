import ipaddress

from django.http import JsonResponse

from ..models import Plugin


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IpRestrictionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_HOST')
        consumer_id = request.META.get('HTTP_CONSUMER_ID')

        plugin_conf = Plugin.objects.filter(
            api__hosts__contains=[host],
            name='ip-restriction'
        ).first()

        if (
            plugin_conf and (
                not plugin_conf.config.get('consumer_id') or
                plugin_conf.config.get('consumer_id') == consumer_id
            )
        ):
            config = plugin_conf.config
            whitelist = config['whitelist']
            blacklist = config['blacklist']
            client_ip = get_client_ip(request)
            if not self.check_ip_address(client_ip, blacklist, whitelist):
                return JsonResponse({'errors': 'Forbidden'}, status=403)

        response = self.get_response(request)

        return response

    def check_ip_address(self, client_ip, blacklist, whitelist):
        client_ip = ipaddress.ip_address(client_ip)
        for ip in blacklist:
            if client_ip in ipaddress.ip_network(ip):
                return False

        if (
            whitelist and
            not any([
                client_ip in
                ipaddress.ip_network(ip) for ip in whitelist
            ])
        ):
            return False
        return True
