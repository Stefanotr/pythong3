from Models.LoginModel import LoginModel
from Views.LoginPageView import LoginPageView
from Utils.Logger import Logger


class LoginController:

    def __init__(self):
        try:
            self.loginModel = LoginModel()
            self.loginView = None
            Logger.debug("LoginController.__init__", "Login controller initialized")
        except Exception as e:
            Logger.error("LoginController.__init__", e)
            raise

    def startLoginFlow(self):
        try:
            self.loginView = LoginPageView(
                "Connexion",
                800,
                800,
                0,
                "Game/Assets/welcomePage.png"
            )

            self.loginView.run()

            return self.loginModel.getCurrentUser()
        except Exception as e:
            Logger.error("LoginController.startLoginFlow", e)
            return None

    def getCurrentUser(self):
        return self.loginModel.getCurrentUser()

    def getUserProgression(self):
        return self.loginModel.getUserProgression()

    def saveProgression(self, progressionData):
        return self.loginModel.saveUserProgression(progressionData)

    def logout(self):
        self.loginModel.logout()
        Logger.debug("LoginController.logout", "User logged out")
