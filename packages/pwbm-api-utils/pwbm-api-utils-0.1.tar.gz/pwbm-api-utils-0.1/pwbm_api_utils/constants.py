from enum import Enum


class APIEnvs(str, Enum):
    dev = 'dev'
    stg = 'stg'


ENV_DATA = {
    APIEnvs.dev: {
        'cognito_client_id': '4a0t0jkdp2g1fbj3prkcd4g1ef',
        'api_prefix': 'https://development.pwbm-api.net/api/v0/explore/',
        'ui_prefix': 'https://dev.pwbm-api.net/',
        'metric_tag_buckets': [
            '2F063138-F1CB-4017-B36E-290FE08F8D94',
            '713FBAA7-FB98-4C0A-BAE7-1C7E8F0A8E75',
        ],
    },
    APIEnvs.stg: {
        'cognito_client_id': '1flh76qlg1no0gfji8c4pcjdje',
        'api_prefix': 'https://staging.pwbm-api.net/api/v0/explore/',
        'ui_prefix': 'https://master.pwbm-api.net/',
        'metric_tag_buckets': [
            'F37DEA97-F7F3-4B0F-A314-9B2359595A79',
            '713FBAA7-FB98-4C0A-BAE7-1C7E8F0A8E75',
        ],
    },
}