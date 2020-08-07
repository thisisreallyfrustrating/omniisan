function enableBtn() {
    document.getElementById("submitbtn").disabled = false;
}


var app = new Vue({
    el: '#app',
    data: {
        makingRequest: false,
        done: false,
        success: false,
        server_message: 'Request sent to server.',
        url: "",
        polling: null,
        storyUrl: ""
    },
    beforeDestroy () {
        clearInterval(this.polling);
    },
    methods: {
        newJob: function () {
            this.makingRequest = true;
            this.requestNewJob();

        },
        closeJob: function () {
            this.makingRequest = false;
            this.done = false;
            this.success = false;
            this.server_message = 'Request sent to server.'
            clearInterval(this.polling);
            this.polling = null;
            this.storyUrl = "";
        },
        requestNewJob: function () {
            recaptchaResponse = grecaptcha.getResponse();
            if (recaptchaResponse === '') {
                this.done = true;
                this.server_message = "You forgot the captcha, you dummy.";
                return;
            }

            axios.post('/jobs',
                       {
                           url: this.url, 
                           'g-recaptcha-response': recaptchaResponse
                       },
                       { headers: {  'Content-Type': 'application/json' } })
                .then(response => {
                    this.done = true;
                    this.success = true;
                    this.server_message = "Task added to queue.";
                    this.pollForUpdates(response.data.task_url);
                })
                .catch(error => {
                    if (error.response) {
                        this.done = true;
                        this.server_message = error.response.data.message;
                    }
                })
        },
        pollForUpdates: function (task_url) {
            this.polling = setInterval( () => {

                axios.get(task_url)
                    .then(response => {
                        this.server_message = response.data.message;
                        // complete success
                        if (response.data.done) {
                            this.storyUrl = response.data.link;
                            clearInterval(this.polling);
                            window.location.assign(this.storyUrl);
                            return;
                        }
                    })
                    .catch(error => {
                            this.done = true;
                        if (error.response) {
                            this.server_message = error.response.data.message;
                        }
                        this.server_message = "Something unexpected has happened...";
                    });
            }, 2000);
        }
    }
});
