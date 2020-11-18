from influxdb import InfluxDBClient


class InfluxProxy(object):
    def __init__(self, domain, database='kubernetes'):
        self.c = InfluxDBClient(database=database)
        self.c._InfluxDBClient__baseurl = domain

    def query(self, q):
        rs = self.c.query(q)
        return rs


if __name__ == '__main__':
    # i = InfluxProxy(domain="http://drycc-monitor-influxdb.uae-t.uucin.com")
    # q = '''SELECT last("rx_bytes") FROM "kubernetes_pod_network"
    #    WHERE ("namespace" = 'py3django3') AND time >= now() - 5m
    #    GROUP BY time(5m), "pod_name" fill(null)'''
    # i.query(q)


    i = InfluxProxy(domain="http://drycc-monitor-influxdb.uae-gs.uucin.com")
    q = '''show tag values from "traefik.service.requests.total" with key = "service"'''
    print(i.query(q))