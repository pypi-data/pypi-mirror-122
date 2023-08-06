from roughrider.cors.policy import CORSPolicy

cors = CORSPolicy(
    methods=['GET', 'POST'],
    allow_headers=['Accept-Encoding'],
    expose_headers=['Accept-Encoding'],
    max_age=19000
)

headers = list(cors.headers())
print(headers)

preflight_headers = list(cors.preflight(
    origin='http://example.com',
    acr_headers='X-Custom-Header, Accept-Encoding'
))
print(preflight_headers)
