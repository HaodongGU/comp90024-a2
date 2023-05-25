## Mastodon Harvester
We implement 2 separate codes to crawl toots from 2 different Mastodon servers.
* Using `Mastodon_Harvester_World_Server.py` to crawl toots from `Mastodon World`
* Using `Mastodon_Harvester_AU_Server.py` to crawl toots from `Mastodon Australia`
Note: All the help functions in above codes are organized in `mastodon_toots_processing.py`

## API Reference

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.

