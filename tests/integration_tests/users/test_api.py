import pytest


@pytest.mark.parametrize(
	"email_reg, password_reg, status_code_register, email_login, password_login, status_code_login",
	[("mama@example.com", "123", 200, "mama@example.com", "123", 200),
	 ("mama2@example.com", "123", 200, "mama2@example.com", "123", 200),
	 ("mama3@example.com", "123", 200, "mama2@example.com", "1234", 401),
	 ])
async def test_user_e2e_flow(ac, email_reg, password_reg, status_code_register, email_login, password_login,
                             status_code_login):
	response_register = await ac.post("/auth/register", json={
		"email": email_reg,
		"password": password_reg
	})
	assert response_register.status_code == status_code_register
	if response_register.status_code == 200:

		response_login = await ac.post("/auth/login", json={
			"email": email_login,
			"password": password_login
		})
		assert response_login.status_code == status_code_login
		if response_login.status_code == 200:
			assert ac.cookies["access_token"] == response_login.json()["access_token"]

			response_get_me = await ac.get("/auth/me")
			assert response_get_me.status_code == status_code_login

			await ac.get("/auth/logout")
			assert ac.cookies == {}
