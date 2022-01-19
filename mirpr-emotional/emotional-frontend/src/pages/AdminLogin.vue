<template>
   <div class="login-page">    
    <div class="wallpaper-login"></div>
    <div class="col-lg-4 col-md-6 col-sm-8 mx-auto">
      <div class="card login">
        <h1>Log In</h1>
        <form class="form-group" @submit="loginSubmit">
          <input  required
            name="username"
            v-model="username"
            placeholder="username"
            type="text"
            autocomplete="off" class="form-control">
          <input  required
            name="password"
            type="password"
            v-model="password"
            placeholder="password"
            autocomplete="off"
            class="form-control">
          <button class="button">Send</button>
        </form>
      </div> 
    </div>
  </div>  
</template>

<script>
export default {
  data() {
    return {
      postAdminLoginUrl: "https://localhost:44373/Login/admin-login/",
      error: "",
      username: "",
      password: "",
    };
  },
  methods: {
    loginSubmit(e) {
      const formData = new FormData();

      e.preventDefault();
      formData.append("username", this.username);
      formData.append("password", this.password);

      fetch(this.postAdminLoginUrl, {
        method: "POST",
        mode: "cors",
        body: formData,
      }).then((response) => {
        if (response.status === 200) this.$router.push("/admin");
      });
    },
  },
};
</script>

<style scoped>
p {
  line-height: 1rem;
}
.card {
  padding: 20px;
  background-color:yellowgreen;
}
.form-control {
  margin-bottom: 20px;
}
.wallpaper-login {
  background-color:rgb(20, 48, 48);
  background-size: cover;
  height: 100%;
  position: absolute;
  width: 100%;
}
.login-page {
  align-items: center;
  display: flex;
  height: 100vh;
}
h1 {
  margin-bottom: 1.5rem;
  color: white;
}
.button{
  padding: 10px 20px;
  border: 1px;
  border-radius: 4px;
  font-size: 14px;
  font-family: '微软雅黑',arail;
  cursor: pointer;
  background-color: #13ce66;
  color: #fff;
}
</style>

