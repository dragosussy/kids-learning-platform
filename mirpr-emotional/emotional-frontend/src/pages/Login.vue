<template>
  <div id="login">
    <img id="attention-grabber" src="./../assets/attention-grabber.gif" />
    <WebCam :autoplay="true" width="auto" :height="windowHeight"></WebCam>
  </div>
</template>

<script>
import { WebCam } from "vue-cam-vision";
//import Compress from 'compress.js'

export default {
  name: "Login",
  components: {
    WebCam,
  },
  data() {
    return {
      postLoginImageUrl: "https://localhost:44373/Login/Login/",
      loginCallInterval: null,
      windowHeight: window.innerHeight,
      windowWidth: window.innerWidth,
    };
  },
  created() {
    // If user has auth_token set already, redirect him to the home page
    const loggedInToken = this.$cookies.get("auth_token");

    const formData = new FormData();
    if (loggedInToken === undefined || loggedInToken === null) return;

    formData.append("loggedInToken", loggedInToken);

    fetch(this.postLoginImageUrl, {
      method: "POST",
      mode: "cors",
      body: formData,
    }).then((response) => {
      if (response.status === 200) this.$router.push("/home");
    });
  },
  mounted() {
    window.addEventListener("resize", () => {
      this.windowHeight = window.innerHeight;
      this.windowWidth = window.innerWidth;
    });

    this.loginCallInterval = setInterval(() => this.captureImage(), 6000); // attempt login every 2 seconds
  },
  beforeDestroy() {
    clearInterval(this.loginCallInterval); // don't make any login calls after the login component is destroyed
  },
  methods: {
    attemptLogin(serverResponse) {
      if (serverResponse.status !== 200) return;

      serverResponse.text().then((authToken) => {
        let authTokenValue = authToken.replaceAll('"', "");

        let expirationDateTime = new Date();
        expirationDateTime.setHours(expirationDateTime.getHours() + 1);

        this.$cookies.set("auth_token", authTokenValue, expirationDateTime);
        this.$router.push("/home");
      });
    },
    uploadImageToServer(img) {
      const formData = new FormData();
      formData.append("file", img);

      fetch(this.postLoginImageUrl, {
        method: "POST",
        mode: "cors",
        body: formData,
      }).then((response) => {
        this.attemptLogin(response);
      });
    },
    async captureImage() {
      let imgBase64 = await this.$children[0].capture();

      await fetch(imgBase64)
        .then(async (response) => {
          let blob = await response.blob();
          const file = new File([blob], "image.jpg", {
            type: "image/jpg",
          });

          return file;
        })
        .then((file) => this.uploadImageToServer(file));
    },
  },
};
</script>

<style scoped>
#attention-grabber {
  position: absolute;

  left: 0;
  top: 0;
  right: 0;

  display: block;
  margin: auto;
  width: 25%;
}
</style>
