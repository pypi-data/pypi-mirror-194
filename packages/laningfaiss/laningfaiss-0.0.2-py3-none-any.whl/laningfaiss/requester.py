import json
from typing import List, Any
from urllib.parse import urljoin
import numpy as np
from httpx import AsyncClient


class Requester:
    def __init__(self, base_url: str, timeout):
        self.base_url = base_url
        self.timeout = timeout

    @staticmethod
    async def request(method, url, **kwargs):
        # XXX: 每次请求都得握手？
        async with AsyncClient() as client:
            response = await client.request(method, url, **kwargs)
        assert response.status_code == 200, f"{response.status_code} {response.reason_phrase}"
        data = json.loads(response.text)
        assert data["code"] == 0, data["msg"]
        return data

    async def get(self, path: str, json=None):
        url = urljoin(self.base_url, path)
        return await self.request("GET", url, json=json, timeout=self.timeout)

    async def post(self, path: str, json=None):
        url = urljoin(self.base_url, path)
        return await self.request("POST", url, json=json, timeout=self.timeout)


class Router:
    def __init__(self, base_url, timeout=10):
        self.requester = Requester(base_url, timeout)

    async def ntotal(self) -> int:
        """
        查询索引中向量的数量
        :return: int
        """
        response = await self.requester.get("ntotal")
        ntotal = response["data"]["ntotal"]
        return int(ntotal)

    async def add(self, ids: List[int], vectors: List[List], train: bool, norm=True) -> bool:
        """
        批量添加向量
        :param ids: 向量id
        :param vectors: 二维向量列表，类型可以是float64,uint8等
        :param train: 是否train， 将质心添加到索引中
        :param norm: 是否要做归一化
        :return: 是否成功
        """
        vectors_arr = np.array(vectors)
        if norm:
            vectors_arr = vectors_arr / np.linalg.norm(vectors_arr, axis=1).reshape(vectors_arr.shape[0], 1)
        payloads = {
            "ids": ids,
            "vectors": vectors_arr.tolist(),
            "train": train
        }
        await self.requester.post("add", json=payloads)
        return True

    async def search(self, vectors: List[List], top_k: int, norm=True) -> List:
        """
        搜索并返回topk结果
        :param vectors: 二维向量列表
        :param top_k: topk的k
        :return: List[List(id: int64, sim: float)]
        :param norm: 是否要做归一化
        """
        vectors_arr = np.array(vectors)
        if norm:
            vectors_arr = vectors_arr / np.linalg.norm(vectors_arr, axis=1).reshape(vectors_arr.shape[0], 1)

        payloads = {
            "vectors": vectors_arr.tolist(),
            "k": top_k
        }
        response = await self.requester.post("search", json=payloads)
        res = response["data"]["res"]
        return res

    async def range_search(self, vectors: List[List], radius: Any, norm=True) -> List:
        """
        搜索并返回范围内的结果
        :param vectors: 二维向量列表
        :param radius: 范围值
        :return: List[List(id: int64, sim: float)]
        :param norm: 是否要做归一化
        """
        vectors_arr = np.array(vectors)
        if norm:
            vectors_arr = vectors_arr / np.linalg.norm(vectors_arr, axis=1).reshape(vectors_arr.shape[0], 1)

        payloads = {
            "vectors": vectors_arr.tolist(),
            "radius": radius
        }
        response = await self.requester.post("range_search", json=payloads)
        res = response["data"]["res"]
        return res

    async def remove(self, ids: List[int]) -> bool:
        """
        根据id删除向量
        :param ids: 向量id列表
        :return: bool
        """
        payloads = {
            "ids": ids,
        }
        await self.requester.post("remove", json=payloads)
        return True

    async def reconstruct(self, ids) -> List[List]:
        """
        根据ids重建向量
        :param ids: 向量id列表
        :return: 二维向量列表，如果向量不存在，返回多个空列表([[], [], [] ...])
        """
        payloads = {
            "ids": ids,
        }
        response = await self.requester.post("reconstruct", json=payloads)
        vectors = response["data"]["vectors"]
        return vectors

    async def info(self) -> tuple:
        """
        获取索引相关信息
        :return: (项目名称, minio地址, 存储到minio的周期<秒>)
        """
        response = await self.requester.get("info")
        data = response["data"]
        return data["name"], data["minio_addr"], data["save_period"]
