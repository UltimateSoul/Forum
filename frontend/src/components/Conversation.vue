<template>
  <div>
    <div class="row">
      <div class="col-lg-8">
        <h1>Conversation</h1>
      </div>
      <div class="col-lg-4">
        <button class="btn btn-dark" @click="createTopic">
          Create Topic
        </button>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12 col-md-10 col-xs-5">
        <table class="table" v-if="!loading">
          <thead>
          <tr>
            <th scope="col">Topic</th>
            <th scope="col">Responses</th>
            <th scope="col">Author</th>
            <th scope="col">Created Date</th>
            <th></th>
          </tr>
          </thead>
          <tbody name="slide" is="transition-group">
            <tr v-for="(topic, index) in topics" :key="topic.posts_quantity">
              <th>{{ topic.title }}</th>
              <td>{{ topic.posts_quantity }}</td>
              <td>{{ topic.author.username }}</td>
              <td>{{ topic.created_date | getDateFormat }}</td>
              <td style="cursor: pointer" @click="remove(index)">
                <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg"
                     xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                     width="20px" height="20px" viewBox="0 0 408.483 408.483"
                     style="enable-background:new 0 0 408.483 408.483;"
                     xml:space="preserve">
<g>
	<g>
		<path d="M87.748,388.784c0.461,11.01,9.521,19.699,20.539,19.699h191.911c11.018,0,20.078-8.689,20.539-19.699l13.705-289.316
			H74.043L87.748,388.784z M247.655,171.329c0-4.61,3.738-8.349,8.35-8.349h13.355c4.609,0,8.35,3.738,8.35,8.349v165.293
			c0,4.611-3.738,8.349-8.35,8.349h-13.355c-4.61,0-8.35-3.736-8.35-8.349V171.329z M189.216,171.329
			c0-4.61,3.738-8.349,8.349-8.349h13.355c4.609,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.737,8.349-8.349,8.349h-13.355
			c-4.61,0-8.349-3.736-8.349-8.349V171.329L189.216,171.329z M130.775,171.329c0-4.61,3.738-8.349,8.349-8.349h13.356
			c4.61,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.738,8.349-8.349,8.349h-13.356c-4.61,0-8.349-3.736-8.349-8.349V171.329z"/>
    <path d="M343.567,21.043h-88.535V4.305c0-2.377-1.927-4.305-4.305-4.305h-92.971c-2.377,0-4.304,1.928-4.304,4.305v16.737H64.916
			c-7.125,0-12.9,5.776-12.9,12.901V74.47h304.451V33.944C356.467,26.819,350.692,21.043,343.567,21.043z"/>
	</g>
</g>
</svg>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios);
  export default {
    name: "Conversation",
    data() {
      return {
        loading: false,
        topics: [],
        testQuantity: 2
      }
    },
    created() {
      this.loading = true;
      this.getData()
    },
    methods: {
      getData() {
        let data = {section: 'IDEAS'};
        Vue.axios.get('http://127.0.0.1:8000/api/conversation/topics/', {params: data})
          .then((resp) => {
            this.topics = resp.data;
          })
          .finally(() => {
            this.loading = false;
          })
      },
      createTopic() {
        // this.$router.push('topic-creation')
        this.topics.push({
          title: 'Test Topic',
          posts_quantity: this.testQuantity,
          author: {
            username: 'Test'
          },
          created_date: '2019-09-14T22:27:18Z'
        });
        this.testQuantity++

      },
      remove(index) {
        this.topics.splice(index, 1)
      }
    },
    filters: {
      getDateFormat(value) {
        let date = new Date(value);
        return date.toLocaleDateString()
      }
    }
  }
</script>

<style scoped>

</style>
