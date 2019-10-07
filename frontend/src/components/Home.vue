<template>
  <div>
    <h1>The Blood Way ORPG 2</h1>
    <div class="row">
      <div class="col-lg-4">
        <div class="card" style="width: 18rem;" v-for="user in users">
          <img :src="user.imageURL" class="card-img-top" alt="...">
          <div class="card-body">
            <h5 class="card-title">{{ user.name }}</h5>
            <p class="card-text">Your level is {{ user.level }}</p>
            <a href="#" class="btn btn-primary">Your Hero: {{ user.hero }}</a>
          </div>
        </div>
      </div>
      <div class="col-lg-8">

      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Home",
    data() {
      return {
        users: [{
          name: 'Pasha',
          level: 1,
          hero: 'Forest Witch',
          imageURL: 'https://i.pinimg.com/originals/96/b9/46/96b946b0f017d8a2681acbe6acbcb50e.jpg'
        },
          {
            name: 'Misha',
            level: 13,
            hero: 'Tree',
            imageURL: 'https://pbs.twimg.com/profile_images/2457288600/dp1ib4f8oefespdd4esy_400x400.jpeg'
          },
          {
            name: 'Soul',
            level: 150,
            hero: 'Bear',
            imageURL: 'https://www.interfax.ru/ftproot/textphotos/2018/07/20/md700.jpg'
          }
        ],
  }}}
</script>

<style scoped>

</style>
