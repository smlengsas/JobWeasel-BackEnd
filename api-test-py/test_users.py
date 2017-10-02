from api_test import ApiTestCase, User


class TestUsers(ApiTestCase):
    def test_sign_up(self):
        used_email = ""
        route = "signUp"

        for data in [self.get_sign_up_data(n) for n in range(1, 3)]:
            used_email = data[User.EMAIL]
            response = self.post(route, data).json()

            self.assertTrue(
                User.SUCCESS in response
            )
            test_user = response[User.USER]
            self.assertEqual(
                test_user[User.NAME], data[User.NAME]
            )
            self.assertEqual(
                test_user[User.EMAIL], data[User.EMAIL]
            )
            self.assertEqual(
                int(test_user[User.ROLE_ID]), data[User.ROLE_ID]
            )

        bad_data = self.get_sign_up_data(1)
        bad_data.pop(User.EMAIL)
        bad_response = self.post(route, bad_data).json()
        self.assertTrue(
            User.ERROR in bad_response
        )

        bad_data[User.EMAIL] = used_email
        response = self.post(route, bad_data).json()
        self.assertTrue(
            User.ERROR in response
        )

    def test_sign_in(self):
        data = self.get_sign_up_data(1)
        self.post('signUp', data).json()
        response = self.post("signIn", data).json()

        self.assertTrue(
            "success" in response
        )
        self.assertTrue(
            "token" in response
        )

        user = self.getUser(response["token"])
        self.assertEqual(
            data["name"], user["name"]
        )

        data["password"] = "wrong"
        bad_response = self.post("signIn", data).json()

        self.assertTrue(
            "error" in bad_response
        )

    def test_show_user(self):
        data = self.get_sign_up_data(1)
        new_user = self.make_new_user(data)

        user_id = new_user["id"]
        response = self.get("showUser/{}".format(user_id)).json()
        user = response["user"]

        self.assertEqual(
            data["name"], user["name"]
        )

    def test_get_users(self):
        data = self.get_sign_up_data(1)
        self.make_new_user(data)

        response = self.get('getUsers').json()
        self.assertTrue(
            "users" in response
        )
        self.assertTrue(
            "data" in response["users"]
        )

    def test_edit_user(self):
        data = self.get_sign_up_data(1)
        token = self.sign_in_new_user(data)

        update_data = self.get_bio_data()
        user = self.post(
            "editUser", update_data, token=token
        ).json()[User.USER]

        self.assertEqual(
            user[User.BIO], update_data[User.BIO]
        )
        self.assertEqual(
            user[User.LOCATION], update_data[User.LOCATION]
        )
        self.assertEqual(
            int(user[User.PHONE]), update_data[User.PHONE]
        )
