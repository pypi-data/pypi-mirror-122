import fire
from opinecli import init, config, auth, project, data, user, subscription, system, organization

__version = "0.2.0"
def version():
    print(f"Opine CLI version {__version}")
list
class Actions(object):
    def __init__(self):
        self.config = config.Config()
        self.auth = auth.SignIn()
        self.project = project.Project()
        self.data = data.Data()
        self.user = user.User()
        self.subscription = subscription.Subscription()
        self.system = system.System()
        self.org = organization.Org()

    def init(self,endpoint="https://api.opine.world"):
        init.Init().start(endpoint)

    def version(self):
        self.version = version()

def main():
    fire.Fire(Actions)

if __name__ == '__main__':
    main()