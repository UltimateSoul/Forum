<template>
<div>
  <div>
    <h1>
      My Team
    </h1>
  </div>
</div>
</template>

<script>
  import axios from 'axios'
  import {mapGetters} from 'vuex'

    export default {
        name: "Team",
      data() {
          return {
            team: {},
            ranks: [],
            maxRanksNumber: 15,
            members: [],
            owner: {}
          }
      },
      created() {
          this.getData()
      },
      methods: {
          getData() {
            return axios.get(`teams/${this.$route.params.teamID}/`)
            .then(
              (response) => {
                debugger;
                switch (response.status) {
                  case 200:
                    break;
                  case 400:
                    break;
                  case 404:
                    break;
                  case 500:
                    break;

                }
              }
            )
          }
      },
      computed: {
          ...mapGetters([
            'getUserData'
          ])
      }
    }
</script>

<style scoped>

</style>
