from bs4 import BeautifulSoup
from locust import HttpUser, task, between
import logging


class QuickstartUser(HttpUser):
    # Random wait time between tasks to simulate realistic user behavior
    wait_time = between(1, 5)

    @task(1)
    def add_a_movie(self):
        """
        Simulates adding a new poll in the 'movies' space
        """
        try:
            # Navigate to space directory (search)
            with self.client.get('/space/browse/search-lazy', catch_response=True) as space_response:
                if "movies" in space_response.text:
                    space_response.success()
                    logging.info("Navigated to space directory successfully.")
                else:
                    space_response.failure("Failed to navigate to space directory.")
                    return

            # Navigate to the 'movies' space
            with self.client.get('/s/movies/', catch_response=True) as movies_response:
                if "/s/movies/about" in movies_response.text:
                    movies_response.success()
                    logging.info("Navigated to movies space successfully.")
                else:
                    movies_response.failure("Failed to navigate to specific space.")
                    return

            # Load the poll creation form
            with self.client.get('/s/movies/polls/poll/create-form', catch_response=True) as form_response:
                if "_csrf" in form_response.text:
                    form_response.success()
                    csrf_token = self.extract_csrf_token(movies_response.text, False)

                    # Prepare data for poll creation
                    new_movies_data = {
                        "_csrf": csrf_token,
                        "Poll[question]": "golzar is good artist ",
                        "Poll[description]": "Description of the artist",
                        "newAnswers[]": ["Perfect", "Good", "Average", "Not good", "Bad"],
                        "Poll[allow_multiple]": 0,
                        "Poll[is_random]": 0,
                        "Poll[anonymous]": 0,
                        "Poll[show_result_after_close]": 0,
                        "postTopicInput[]": [2, 3, 4],
                        "containerGuid": "6b81cf24-03e2-4398-9a9c-11f4ac8574ae",
                        "containerClass": "humhub%5Cmodules%5Cspace%5Cmodels%5CSpace",
                        "state": 1
                    }
                else:
                    form_response.failure("CSRF token not found in form.")
                    return

                # Submit the poll creation request
                with self.client.post('/s/movies/polls/poll/create', data=new_movies_data, catch_response=True) as polls_response:
                    if 'guid' in polls_response.text:
                        logging.info("[+] Added a movie")
                        polls_response.success()
                    else:
                        polls_response.failure("Failed to create poll.")

        except Exception as e:
            logging.exception("An error occurred during the process")

    @task(2)
    def messaging(self):
        """
        Simulates sending a message in a chat
        """
        # Open mailbox
        with self.client.get('/mail/mail/index', catch_response=True) as mail_response:
            if mail_response.status_code == 200:
                mail_response.success()
                logging.info("[+] Mailbox opened.")
                csrf_token = self.extract_csrf_token(mail_response.text, True)
            else:
                mail_response.failure("Failed to open mailbox.")
                return

        # Open chat thread
        with self.client.get('/mail/mail/show?id=1', catch_response=True) as group_response:
            if group_response.status_code == 200:
                group_response.success()
                logging.info("[+] Chat box opened.")
                self.client.headers["X-CSRF-Token"] = csrf_token
                message_data = {
                    "ReplyForm[message]": "This is a message from Locust. from messaging"
                }
            else:
                group_response.failure("Failed to open the chat.")
                return

        # Send the message
        with self.client.post("/mail/mail/reply?id=1", data=message_data, catch_response=True) as message_response:
            if message_response.status_code == 200:
                logging.info("[+] Message sent successfully.")
                message_response.success()
            else:
                message_response.failure("Failed to send message.")

        self.client.headers.pop("X-CSRF-Token")

    @task(4)
    def leave_a_comment(self):
        """
        Simulates posting a comment on a poll
        """
        # Load dashboard and extract CSRF token
        with self.client.get('/dashboard', catch_response=True) as response:
            if response.status_code == 200 and "csrf" in response.text:
                response.success()
                csrf_token = self.extract_csrf_token(response.text, True)
            else:
                response.failure("Couldn't load dashboard.")
                return

        # Load latest stream entries
        with self.client.get("/dashboard/dashboard/stream?StreamQuery%5Bfrom%5D=0&StreamQuery%5Blimit%5D=10", catch_response=True) as dashboard_update:
            dashboard_update.success()
            object_model = 'humhub\\modules\\polls\\models\\Poll'
            comment_data = {
                "objectModel": object_model,
                "objectId": 8,
                "Comment[message]": "This is an automated comment from Locust. with leaving"
            }
            self.client.headers["X-CSRF-Token"] = csrf_token

        # Submit the comment
        with self.client.post("/comment/comment/post", data=comment_data, catch_response=True) as comment_response:
            if comment_response.status_code == 200:
                comment_response.success()
                logging.info("[+] Comment posted.")
            else:
                comment_response.failure("Failed to post comment.")

        self.client.headers.pop("X-CSRF-Token")

    @task(5)
    def check_movies_space(self):
        """
        Simulates checking the 'movies' space
        """
        with self.client.get('/space/browse/search-lazy', catch_response=True) as jresponse:
            if "movies" in jresponse.text:
                jresponse.success()
                with self.client.get('/s/movies/', catch_response=True) as space_response:
                    if space_response.status_code == 200:
                        space_response.success()
                        logging.info("[+] Movies space checked successfully.")
                    else:
                        space_response.failure("[-] Failed to load movies space.")
            else:
                jresponse.failure("[-] Space search failed.")

    @task(6)
    def full_post(self):
        """
        Simulates viewing a specific post by permalink
        """
        with self.client.get('/dashboard', catch_response=True) as dashboard_response:
            if dashboard_response.status_code == 200:
                dashboard_response.success()
            else:
                dashboard_response.failure("[-] Dashboard load failed.")
                return

        with self.client.get('/content/perma?id=24', catch_response=True) as post_response:
            if post_response.status_code == 200:
                post_response.success()
                logging.info("[+] Viewed a full post.")
            else:
                post_response.failure("Failed to open post.")

    @task(10)
    def check_dashboard(self):
        """
        Simulates a user checking the dashboard
        """
        with self.client.get('/dashboard', catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                logging.info("[+] Dashboard checked successfully.")
            else:
                response.failure("[-] Dashboard access failed.")

    def on_stop(self):
        """
        Logs the user out after test execution
        """
        with self.client.get('/dashboard', catch_response=True) as dresponse:
            if dresponse.status_code == 200:
                csrf_token = self.extract_csrf_token(dresponse.text, True)
                with self.client.post('/user/auth/logout', data={"_csrf": csrf_token}, catch_response=True) as log_response:
                    if "login" in log_response.text:
                        logging.info("[+] Logout successful.")
                    else:
                        log_response.failure("[-] Logout failed.")
            else:
                dresponse.failure("[-] Failed to load dashboard before logout.")

    def extract_csrf_token(self, html_content, is_meta: bool):
        """
        Extracts CSRF token from a page, either from <meta> or <input> field
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        if is_meta:
            return soup.find('meta', {'name': 'csrf-token'})['content']
        else:
            return soup.find('input', {'name': '_csrf'})['value']

    def on_start(self):
        """
        Logs in the user before test execution begins
        """
        with self.client.get('/user/auth/login', catch_response=True) as Gresponse:
            if Gresponse.status_code == 200:
                csrf_token = self.extract_csrf_token(Gresponse.text, False)
                with self.client.post("/user/auth/login", data={
                    "_csrf": csrf_token,
                    "Login[username]": "mojtaba",
                    "Login[password]": "123456789",
                    "Login[rememberMe]": "1"
                }, catch_response=True) as response:
                    if response.status_code == 200 and "logout" in response.text:
                        response.success()
                    else:
                        response.failure("[-] Login failed.")
            else:
                Gresponse.failure("[-] Couldn't load login page.")




