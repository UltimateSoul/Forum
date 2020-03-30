<template>
  <div>
    <h1>{{topic.title}}</h1>
    <hr>
    <h5>{{topic.description}}</h5>
    <div>
      <b-card no-body class="overflow-hidden">
        <b-row no-gutters>
          <b-col md="2">
            <b-card-img :src="author.avatar" class="rounded-1"></b-card-img>
            <h5>{{author.username}}</h5>
            <h5>{{author.gameNickName}}</h5>
          </b-col>
          <b-col md="10">
            <b-card-body>
              <b-card-text>
                {{topic.body}}
              </b-card-text>
            </b-card-body>
          </b-col>
        </b-row>
        Likes: {{topic.totalLikes}}
        <b-button variant="primary"
                  :pressed="topic.isLiked"
                  @click="likeOrUnlikeTopicClick()"
                  :id="'like-topic-button-' + topicID">
          Like
        </b-button>
      </b-card>
      <div class="button-control" v-if="isMainUser(author.pk)">
        <b-button @click="editTopic">Edit</b-button>
      </div>
      <div v-for="post in posts"
           :key="post.id">
        <hr>
        <b-card no-body class="overflow-hidden">
          <b-row no-gutters>
            <b-col md="2">
              <b-card-img :src="post.author.avatar" class="rounded-1"></b-card-img>
            </b-col>
            <b-col md="10">
              <b-card-body :title="post.author.username">
                <b-card-text>
                  {{post.body}}
                </b-card-text>
              </b-card-body>
            </b-col>
            Likes: {{post.total_likes}}
          </b-row>
          <div class="button-control">
            <b-button variant="primary"
                      :pressed="post.is_liked"
                      @click="likeOrUnlikePostClick(post.id, post.is_liked)"
                      :id="'like-post-button-' + post.id">
              Like
            </b-button>
          </div>
        </b-card>
        <div class="button-control">
          <b-button variant="primary"
                    @click="buttonsEngine['button-'+post.id].isOpen = !buttonsEngine['button-'+post.id].isOpen"
                    :id="'button-' + post.id">
            {{ getCommentsButtonText('button-' + post.id) }}
          </b-button>
        </div>
        <div v-if="buttonsEngine['button-'+post.id].isOpen">
          <div class="message-range" v-for="comment in post.comments">
            <b-card no-body class="overflow-hidden">
              <b-row no-gutters>
                <b-col md="2">
                  <b-card-img :src="comment.author.avatar" class="rounded-1"></b-card-img>
                </b-col>
                <b-col md="10">
                  <b-card-body :title="comment.author.username">
                    <b-card-text>
                      {{comment.body}}
                    </b-card-text>
                  </b-card-body>
                </b-col>
              </b-row>
              Likes: {{comment.total_likes}}
              <div class="button-control">

                <b-button :pressed="comment.is_liked"
                          variant="primary"
                          @click="likeOrUnlikeCommentClick(comment.id, comment.is_liked)"
                          :id="'like-comment-button-' + comment.id">
                  Like
                </b-button>
              </div>
            </b-card>
          </div>
          <div class="message-range">
            <b-form-textarea
              id="textarea"
              v-model="commentText"
              placeholder="Enter comment..."
              rows="3"
              max-rows="6"
            ></b-form-textarea>
            <b-button variant="primary"
                      @click="saveComment(post.id)"
                      :id="'button-comment' + post.id">
              Post
            </b-button>
          </div>
        </div>
      </div>
      <div class="message-range">
        <b-form-textarea
          id="textarea"
          v-model="postText"
          placeholder="Enter post..."
          rows="3"
          max-rows="6"
        ></b-form-textarea>
        <b-button @click="savePost" variant="primary">
          Post
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {mapGetters} from 'vuex';

  export default {
    name: "Topic",
    data() {
      return {
        topicID: this.$route.params.topicID,
        topic: {
          title: "",
          description: "",
          body: "",
          totalLikes: 0,
          isLiked: false
        },
        author: {
          avatar: '',
          gameNickName: '',
          username: '',
          pk: 0
        },
        posts: [],
        buttonsEngine: {},
        postText: '',
        commentText: '',
        currentPage: 1
      }
    },
    created() {
      this.getTopicData();
      this.getTopicPosts(1)
    },
    methods: {
      getTopicData() {
        axios.get('topic/get/' + this.topicID + '/').then(
          (response) => {
            this.topic.title = response.data.title;
            this.topic.description = response.data.description;
            this.topic.body = response.data.body;
            this.topic.totalLikes = response.data.total_likes;
            this.topic.isLiked = response.data.is_liked;
            this.author.avatar = response.data.author.avatar;
            this.author.gameNickName = response.data.author.game_nickname;
            this.author.username = response.data.author.username;
            this.author.pk = response.data.author.pk;
            this.title = response.data.title;
          }
        )
      },
      getTopicPosts(page) {
        axios.get('posts/', {
          params: {
            topic: this.topicID,
            page: page,
          }
        }).then((response) => {
          this.posts = response.data.results;
          this.posts.forEach(post => {
            let buttonID = 'button-' + post.id;
            this.$set(this.buttonsEngine, buttonID, {
              isOpen: false
            })
          })
        })
      },
      editTopic() {
        this.$router.push({
          name: 'topic-editing',
          params: {
            section: this.$route.params.section,
            topicID: this.topicID
          }
        })
      },
      saveComment(postID) {
        const data = {
          body: this.commentText,
          post: postID
        };
        axios.post('comments/', data)
          .then((response) => {
            debugger
            switch (response.status) {
              case 201:
                this.commentText = '';
                this.getTopicPosts(this.currentPage);
                break;
              case 400:
                break
            }
          })
      },
      savePost() {
        const data = {
          body: this.postText,
          topic: this.topicID
        };
        axios.post('posts/', data)
          .then((response) => {
            switch (response.status) {
              case 201:
                this.postText = '';
                this.getTopicPosts(this.currentPage);
                break;
              case 400:
                break
            }
          })
      },
      likeOrUnlikePostClick(postID, isLiked) {
        if (isLiked) {
          axios.post(`posts/${postID}/unlike/`)
            .then((response) => {
              switch (response.status) {
                case 200:
                  this.getTopicPosts(this.currentPage);
                  break;
                case 400:
                  break  // errors during serializing
              }
            })
        } else {
          axios.post(`posts/${postID}/like/`)
            .then((response) => {
              switch (response.status) {
                case 201:
                  this.getTopicPosts(this.currentPage);
                  break;
                case 220:
                  break;  // already liked this post by current user
                case 400:
                  break  // errors during serializing
              }
            })
        }
      },
      likeOrUnlikeCommentClick(commentID, isLiked) {
        if (isLiked) {
          axios.post(`comments/${commentID}/unlike/`)
            .then((response) => {
              switch (response.status) {
                case 200:
                  this.getTopicPosts(this.currentPage);
                  break;
                case 400:
                  break  // errors during serializing
              }
            })
        }
        axios.post(`comments/${commentID}/like/`)
          .then((response) => {
            switch (response.status) {
              case 201:
                this.getTopicPosts(this.currentPage);
                break;
              case 220:
                break;  // already liked this post by current user
              case 400:
                break  // errors during serializing
            }
          })
      },
      likeOrUnlikeTopicClick() {
        if (this.topic.isLiked) {
          axios.post(`topic/unlike/${this.topicID}/`).then((response) => {
            switch (response.status) {
              case 200:
                this.getTopicData();
                break;
              case 400:
                break  // errors during serializing
            }
          })
        } else {
          axios.post(`topic/like/${this.topicID}/`).then((response) => {
            switch (response.status) {
              case 201:
                this.getTopicData();
                break;
              case 220:
                break;  // already liked this post by current user
              case 400:
                break  // errors during serializing
            }
          })
        }
      }
    },
    computed: {
      ...mapGetters([
        'isMainUser',
        'getUserData'
      ]),
      getCommentsButtonText() {
        return buttonID => {
          console.log('getCommentsButtonText');
          let isOpen = this.buttonsEngine[buttonID].isOpen;
          return isOpen ? 'Collapse' : 'Expand'

        }
      },
    }
  }
</script>

<style scoped>
  .message-range {
    margin: 10px 15%;
  }
</style>
