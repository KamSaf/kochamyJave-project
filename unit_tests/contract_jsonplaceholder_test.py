import json
import requests
import unittest


class JSONPlaceholderContractTest(unittest.TestCase):
    def test_requested_post(self):
        expected_post = {
              "userId": 1,
              "id": 1,
              "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
              "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut "
                      "ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto "
        }
        api_response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        data = api_response.text
        post = json.loads(data)
        self.assertEqual(post, expected_post)

    def test_requested_comments(self):
        expected_post = [
                    {
                        "postId": 1,
                        "id": 1,
                        "name": "id labore ex et quam laborum",
                        "email": "Eliseo@gardner.biz",
                        "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo "
                                "necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium "
                    },
                    {
                        "postId": 1,
                        "id": 2,
                        "name": "quo vero reiciendis velit similique earum",
                        "email": "Jayne_Kuhic@sydney.com",
                        "body": "est natus enim nihil est dolore omnis voluptatem numquam\net omnis occaecati quod "
                                "ullam at\nvoluptatem error expedita pariatur\nnihil sint nostrum voluptatem "
                                "reiciendis et "
                    },
                    {
                        "postId": 1,
                        "id": 3,
                        "name": "odio adipisci rerum aut animi",
                        "email": "Nikita@garfield.biz",
                        "body": "quia molestiae reprehenderit quasi aspernatur\naut expedita occaecati aliquam "
                                "eveniet laudantium\nomnis quibusdam delectus saepe quia accusamus maiores nam "
                                "est\ncum et ducimus et vero voluptates excepturi deleniti ratione "
                    },
                    {
                        "postId": 1,
                        "id": 4,
                        "name": "alias odio sit",
                        "email": "Lew@alysha.tv",
                        "body": "non et atque\noccaecati deserunt quas accusantium unde odit nobis qui "
                                "voluptatem\nquia voluptas consequuntur itaque dolor\net qui rerum deleniti ut "
                                "occaecati "
                    },
                    {
                        "postId": 1,
                        "id": 5,
                        "name": "vero eaque aliquid doloribus et culpa",
                        "email": "Hayden@althea.biz",
                        "body": "harum non quasi et ratione\ntempore iure ex voluptates in ratione\nharum architecto "
                                "fugit inventore cupiditate\nvoluptates magni quo et "
                    }
            ]
        api_response = requests.get('https://jsonplaceholder.typicode.com/posts/1/comments')
        data = api_response.text
        post = json.loads(data)
        self.assertEqual(post, expected_post)


if __name__ == '__main__':
    unittest.main()
