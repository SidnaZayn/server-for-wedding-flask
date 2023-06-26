
# Wedding of Sidna and Ariesty Back-End

it's a back end project for wedding invitation of Sidna and Ariesty using Flask and MySql DB


## API Reference

#### Get all items

```http
  GET /api/1.0/lihat_data_tamu
```

#### Get one guest

```http
  GET /api/1.0/lihat_data_satu_tamu
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Post guest

```http
  POST /api/1.0/tambah_tamu
```

| Parameter | Type     | 
| :-------- | :------- | 
| `nama`      | `string` | 
| `alamat`      | `string` |
| `jenis_tamu`      | `string` |


```http
  POST /api/1.0/edit_data_tamu
```

| Parameter | Type     | 
| :-------- | :------- | 
| `id`      | `int` | 
| `nama`      | `string` | 
| `alamat`      | `string` |
| `jenis_tamu`      | `string` |

## RUN PROJECT
```http
  http://127.0.0.1:8008
```

## has'nt been created features
