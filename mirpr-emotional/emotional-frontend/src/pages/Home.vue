<template>
  <div id="home">
    <span id="main">
      <div id="games">
        <img id="attention-grabber" src="./../assets/attention-grabber.gif" />
        <a
          href="https://wordwall.net/ro/resource/9632446/jocuri-de-iarna-pentru-copii"
          target="_blank"
          @click="redirectToActivity"
          activityName="jocuri-iarna"
          >Jocuri de iarna</a
        >
        <a
          href="https://academiaabc.ro/jocuri_de_memorie/forme-geometrice/"
          target="_blank"
          @click="redirectToActivity"
          activityName="forme-geometrice"
          >Forme geometrice</a
        >
        <a href="https://www.youtube.com/watch?v=bovkOVCtSb4" target="_blank"
          >Desene animate cu pisici</a
        >
        <a
          href="https://www.cartoonnetwork.ro/jocuri/aventurile-fratilor-ursi-cum-sa-desenezi-ursul-polar/joaca"
          target="_blank"
          @click="redirectToActivity"
          activityName="deseneaza-urs-polar"
          >Deseneaza ursul polar</a
        >
        <a
          href="https://www.jigsawplanet.com/?rc=play&pid=27db980a3162"
          target="_blank"
          @click="redirectToActivity"
          activityName="puzzle-craciun"
          >Puzzle de Craciun</a
        >
        <a
          href="https://games.cdn.famobi.com/html5games/k/kids-block-puzzle/v120/?fg_domain=play.famobi.com&fg_aid=A-MJ4VU&fg_uid=d28ef57e-ab53-47f0-b64a-a35841c9ef2b&fg_pid=f8e4f1f1-d1ee-4bc4-b94a-7ab84ea26b14&fg_beat=698&original_ref=https%3A%2F%2Fwww.kidsworldfun.com%2F"
          target="_blank"
          @click="redirectToActivity"
          activityName="puzzle-pisici"
          >Puzzle cu pisici</a
        >
        <a
          href="https://games.cdn.famobi.com/html5games/0/123-puzzle/v030/?fg_domain=play.famobi.com&fg_aid=A-MJ4VU&fg_uid=859e7036-2740-47b3-9e9d-2aeb90853a4c&fg_pid=f8e4f1f1-d1ee-4bc4-b94a-7ab84ea26b14&fg_beat=699&original_ref=https%3A%2F%2Fwww.kidsworldfun.com%2F"
          target="_blank"
          @click="redirectToActivity"
          activityName="quizz-numere"
          >Quizz cu numere</a
        >
      </div>
      <WebCam :autoplay="true" width="auto" :height="windowHeight"></WebCam>
    </span>
  </div>
</template>

<script>
import { WebCam } from "vue-cam-vision";
import $ from "jquery";

export default {
  name: "Home",
  components: {
    WebCam,
  },
  data() {
    return {
      postEmotionRecognitionImageUrl:
        "https://localhost:44373/FaceRecognition/recognize-emotions/",
      windowHeight: window.innerHeight,
      windowWidth: window.innerWidth,
      recognizeFaceInterval: null,
      activity: "none",
    };
  },
  mounted() {
    window.addEventListener("resize", () => {
      this.windowHeight = window.innerHeight;
      this.windowWidth = window.innerWidth;
    });

    this.recognizeFaceInterval = setInterval(() => this.captureImage(), 10000);
    // setTimeout(() => this.captureImage(), 5000);
  },
  beforeDestroy() {
    clearInterval(this.recognizeFaceInterval);
  },
  methods: {
    uploadImageToServer(img) {
      const loggedInToken = this.$cookies.get("auth_token");

      const formData = new FormData();
      formData.append("file", img);
      formData.append("sessionToken", loggedInToken);
      formData.append("activity", this.activity);

      fetch(this.postEmotionRecognitionImageUrl, {
        method: "POST",
        mode: "cors",
        body: formData,
      }).then((response) => {
        console.log(response);
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
    redirectToActivity(e) {
      this.activity = $(e.path[0]).attr("activityName");
    },
  },
};
</script>

<style scoped>
#main {
  display: flex;
}
#games {
  margin-right: 80px;
  margin-left: 40px;
}
a {
  display: block;
  background-color: yellowgreen;
  margin: 15%;
  border-radius: 5px;
}
#attention-grabber {
  height: 100px;
}
</style>
