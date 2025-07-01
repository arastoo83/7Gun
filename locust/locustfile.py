from bs4 import BeautifulSoup
from locust import HttpUser, task, between
import logging


class QuickstartUser(HttpUser):
    # Random wait time between tasks to simulate realistic user behavior
    wait_time = between(1 , 5)

    @task(1)
    def add_a_artist(self):
        """
        Simulates adding a new poll in the 'artist and car' space
        """
        try:

            # Navigate to space directory (search)
            with self.client.get('/space/browse/search-lazy', catch_response=True) as space_response:
                if "artist" in space_response.text:
                    space_response.success()
                    logging.info("Navigated to space directory successfully.")
                else:
                    space_response.failure("Failed to navigate to space directory.")
                    return

            # Navigate to the 'artist' space
            with self.client.get('/s/artist/', catch_response=True) as artist_response:
                if "/s/artist/about" in artist_response.text:
                    artist_response.success()
                    logging.info("Navigated to artist space successfully.")
                else:
                    artist_response.failure("Failed to navigate to specific space.")
                    return

            # Load the poll creation form
            with self.client.get('/s/artist/polls/poll/create-form', catch_response=True) as form_response:
                if "_csrf" in form_response.text:
                    form_response.success()
                    csrf_token = self.extract_csrf_token(artist_response.text, False)

                    # Prepare data for poll creation
                    new_artist_data = {
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
                with self.client.post('/s/artist/polls/poll/create', data=new_artist_data, catch_response=True) as polls_response:
                    if 'guid' in polls_response.text:
                        logging.info("[+] Added a artist")
                        polls_response.success()
                    else:
                        polls_response.failure("Failed to create poll.")

                # follow the pepole 
                with self.client.post('/u/david1986/user/profile/follow', data=new_artist_data, catch_response=True) as follow_response:
                    if 'guid' in follow_response.text:
                        logging.info("[+] follow the david")
                        follow_response.success()
                    else:
                        follow_response.failure("Failed to follow david.")
                # unfollow the pepole                                 
                with self.client.post('/u/david1986/user/profile/unfollow', data=new_artist_data, catch_response=True) as unfollow_response:
                    if 'guid' in unfollow_response.text:
                        logging.info("[+] unfollow the david")
                        unfollow_response.success()
                    else:
                        unfollow_response.failure("Failed to unfollow david.")   
        except Exception as e:
            logging.exception("An error occurred during the process")



    @task(1)
    def add_a_car(self):
        """
        Simulates adding a new poll in the ' car' space
        """
        try:

            # Navigate to space directory (search)
            with self.client.get('/space/browse/search-lazy', catch_response=True) as space_Car_response:
                if "car" in space_Car_response.text:
                    space_Car_response.success()
                    logging.info("Navigated to space Car directory successfully.")
                else:
                    space_Car_response.failure("Failed to navigate to space Car directory.")
                    return

            # Navigate to the 'Car' space
            with self.client.get('/s/car/', catch_response=True) as Car_response:
                if "/s/car/about" in Car_response.text:
                    Car_response.success()
                    logging.info("Navigated to Car space successfully.")
                else:
                    Car_response.failure("Failed to navigate to specific space.")
                    return

            # Load the poll creation form
            with self.client.get('/s/car/polls/poll/create-form', catch_response=True) as form_Car_response:
                if "_csrf" in form_Car_response.text:
                    form_Car_response.success()
                    csrf_token = self.extract_csrf_token(form_Car_response.text, False)

                    # Prepare data for poll creation
                    new_Car_data = {
                        "_csrf": csrf_token,
                        "Poll[question]": "Whats is the Best Car in the World? ",
                        "Poll[description]": "Description of the Car",
                        "newAnswers[]": ["Bugatti", "Lamborghini", "Samand Soren", "Pride", "Peugeot405"],
                        "Poll[allow_multiple]": 0,
                        "Poll[is_random]": 0,
                        "Poll[anonymous]": 0,
                        "Poll[show_result_after_close]": 0,
                        "postTopicInput[]": [2, 3, 4],
                        "containerGuid": "bec99480-3074-4a46-b6f9-d76ea4789f2e",
                        "containerClass": "humhub%5Cmodules%5Cspace%5Cmodels%5CSpace",
                        "state": 1
                    }
                else:
                    form_Car_response.failure("CSRF token not found in form.")
                    return

                # Submit the poll creation request
                with self.client.post('/s/car/polls/poll/create', data=new_Car_data, catch_response=True) as polls_Car_response:
                    if 'guid' in polls_Car_response.text:
                        logging.info("[+] Added a Car")
                        polls_Car_response.success()
                    else:
                        polls_Car_response.failure("Failed to create poll Car.")
        except Exception as e:
            logging.exception("An error occurred during the process")

    @task(1)
    def add_a_post(self):
        """
        Simulates adding a new post
        """
        try:
            # Load the page for make new post
            with self.client.get('/u/mojtaba/', catch_response=True) as form_post_response:
                if "_csrf" in form_post_response.text:
                    form_post_response.success()
                    csrf_token = self.extract_csrf_token(form_post_response.text, False)

                    # Prepare data for post creation
                    new_artist_data = {
                        "_csrf": csrf_token,
                        "Post[message]": "This is a new post created via Locust.",
                        "containerGuid": "10c7c3fb-5169-499e-a9c0-973bebf2fe5c",  
                        "containerClass": "humhub/modules/user/models/User",  
                        "visibility": 1 ,
                        "state": 1
                    }
                else:
                    form_post_response.failure("CSRF token not found in form.")
                    return

                # Submit the post creation request
                with self.client.post('/u/mojtaba/post/post/post', data=new_artist_data, catch_response=True) as po_response:
                    if 'guid' in po_response.text:
                        logging.info("[+] Added a post")
                        po_response.success()
                    else:
                        po_response.failure("Failed to create post.")

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
                    "ReplyForm[message]": "This is a message from Locust. for testing"
                }
            else:
                group_response.failure("Failed to open the chat.")
                return
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
                "objectId": 14,
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

        # like the comment
        with self.client.post("/like/like/like?contentModel=humhub%5Cmodules%5Cpolls%5Cmodels%5CPoll&contentId=14", data=comment_data, catch_response=True) as like_comment:
            if like_comment.status_code == 200:
                like_comment.success()
                logging.info("[+] like Comment .")
            else:
                like_comment.failure("Failed to like comment.")

        # unlike the comment
        with self.client.post("/like/like/unlike?contentModel=humhub%5Cmodules%5Cpolls%5Cmodels%5CPoll&contentId=14", data=comment_data, catch_response=True) as like_comment:
            if like_comment.status_code == 200:
                like_comment.success()
                logging.info("[+] unlike Comment .")
            else:
                like_comment.failure("Failed to unlike comment.")

        self.client.headers.pop("X-CSRF-Token")

    @task(5)
    def check_artist_space(self):
        """
        Simulates checking the 'artist' space and people
        """
        #search a space exmple artist with lazy search
        with self.client.get('/space/browse/search-lazy', catch_response=True) as jresponse:
            if "artist" in jresponse.text:
                jresponse.success()
                with self.client.get('/s/artist/', catch_response=True) as space_response:
                    if space_response.status_code == 200:
                        space_response.success()
                        logging.info("[+] artist space checked successfully.")
                    else:
                        space_response.failure("[-] Failed to load artist space.")
            else:
                jresponse.failure("[-] Space search failed.")

        #search a people exmple David Robets with normal search
        with self.client.get('/people?keyword=David Roberts', catch_response=True) as jresponse_two:
            if "David Roberts" in jresponse_two.text:
                jresponse_two.success()
                with self.client.get('/u/david1986/', catch_response=True) as people_search:
                    if people_search.status_code == 200:
                        people_search.success()
                        logging.info("[+] David Roberts checked successfully.")
                    else:
                        people_search.failure("[-] Failed to load David Roberts.")
            else:
                jresponse_two.failure("[-] David Roberts search failed.")

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




