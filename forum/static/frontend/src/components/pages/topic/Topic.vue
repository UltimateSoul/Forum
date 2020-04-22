<template>
  <div>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="15"
      aria-controls="my-table"
    ></b-pagination>
    <h1>{{topic.title}}</h1>
    <hr>
    <h5>{{topic.description}}</h5>
    <modal name="deleteModal">
      <div class="m-5 text-center">
        <h1>
          Are you sure?
        </h1>
        <h4>
          Are you really sure that you want to delete this topic? All you actions will be recorded.
        </h4>
        <b-row>
          <b-col>
            <b-button variant="dark" @click="hideDeleteModal">Cancel</b-button>
          </b-col>
          <b-col>
            <b-button variant="dark" @click="moderatorDeleteTopic">Delete</b-button>
          </b-col>
        </b-row>
      </div>
    </modal>
    <div>
      <b-card no-body class="overflow-hidden">
        <b-row no-gutters>
          <b-col md="2">
            <b-card-img :src="author.avatar" class="rounded-1"></b-card-img>
            <h5>{{author.username}}</h5>
            <hr>
            <b-row>
              <b-col @click="profileClick(author.pk)">
                <Profile></Profile>
              </b-col>
              <b-col></b-col>
              <b-col></b-col>
            </b-row>
          </b-col>
          <b-col md="10">
            <b-card-body>
              <b-card-text>
                <div class="html-text" v-html="topic.body"></div>
              </b-card-text>
            </b-card-body>
          </b-col>
        </b-row>
        <hr>
        <b-row>
          <b-col></b-col>
          <b-col>
            <div v-if="isModerator">
              <b-button v-b-toggle.collapse-1 variant="dark">Moderator Actions</b-button>
              <b-collapse id="collapse-1" class="mt-2">
                <b-card>
                  <b-row>
                    <b-col>
                      <div class="clickable" @click="showDeleteModal">
                        <delete-topic-button></delete-topic-button>
                      </div>
                    </b-col>
                    <b-col>
                      <div class="clickable" @click="editTopic">
                        <edit-topic-button></edit-topic-button>
                      </div>
                    </b-col>
                  </b-row>
                </b-card>
              </b-collapse>
            </div>
          </b-col>
          <b-col>
            <b-button variant="dark"
                      :pressed="topic.isLiked"
                      @click="likeOrUnlikeTopicClick"
                      :id="'like-topic-button-' + topicID">
              {{ topic.isLiked ? 'Unlike' : 'Like' }}
            </b-button>
            {{topic.totalLikes}}
          </b-col>
        </b-row>
      </b-card>
      <div class="button-control" v-if="isMainUser(author.pk)">
        <b-button @click="editTopic">Edit</b-button>
      </div>
      <div v-if="loading">
        <b-spinner class="spinner-style" label="Loading..."></b-spinner>
      </div>
      <div v-else>
        <div v-for="post in posts"
             :key="post.id">
          <hr>
          <b-card no-body class="overflow-hidden">
            <b-row no-gutters>
              <b-col md="2">
                <b-card-img :src="post.author.avatar" class="rounded-1"></b-card-img>
                <h5>{{ post.author.username }}</h5>
                <hr>
                <b-row>
                  <b-col @click="profileClick(post.author.id)">
                    <Profile></Profile>
                  </b-col>
                  <b-col></b-col>
                  <b-col></b-col>
                </b-row>
              </b-col>
              <b-col md="10">
                <b-card-body>
                  <div class="html-text" v-html="post.body"></div>
                </b-card-body>
              </b-col>
            </b-row>
            <div class="button-control">
              <b-button variant="dark"
                        :pressed="post.is_liked"
                        @click="likeOrUnlikePostClick(post.id, post.is_liked)"
                        :id="'like-post-button-' + post.id">
                {{ post.is_liked ? 'Unlike' : 'Like' }}
              </b-button>
              {{post.total_likes}}
            </div>
          </b-card>
          <div class="button-control">
            <b-button variant="dark"
                      :class="buttonsEngine['button-'+post.id].isOpen ? null : 'collapsed'"
                      :aria-expanded="buttonsEngine['button-'+post.id].isOpen ? 'true' : 'false'"
                      :aria-controls="'collaps-' + post.id"
                      @click="buttonsEngine['button-'+post.id].isOpen = !buttonsEngine['button-'+post.id].isOpen"
                      :id="'button-' + post.id">
              {{ getCommentsButtonText('button-' + post.id) }}
            </b-button>
          </div>
          <b-collapse :id="'collaps-' + post.id" v-model="buttonsEngine['button-'+post.id].isOpen" class="mt-2">
            <div class="message-range" v-for="comment in post.comments">
              <b-card no-body class="overflow-hidden">
                <b-row no-gutters>
                  <b-col md="2">
                    <b-card-img :src="comment.author.avatar" class="rounded-1"></b-card-img>
                    <h5>{{comment.author.username}}</h5>
                    <hr>
                    <b-row>
                      <b-col @click="profileClick(post.author.id)">
                        <Profile></Profile>
                      </b-col>
                      <b-col></b-col>
                      <b-col></b-col>
                    </b-row>
                  </b-col>
                  <b-col md="10">
                    <b-card-body>
                      <b-card-text>
                        <div class="html-text" v-html="comment.body"></div>
                      </b-card-text>
                    </b-card-body>
                  </b-col>
                </b-row>
                Likes: {{comment.total_likes}}
                <div class="button-control">
                  <b-button :pressed="comment.is_liked"
                            variant="dark"
                            @click="likeOrUnlikeCommentClick(comment.id, comment.is_liked)"
                            :id="'like-comment-button-' + comment.id">
                    {{ comment.is_liked ? 'Unlike' : 'Like' }}
                  </b-button>
                </div>
              </b-card>
            </div>
            <div class="message-range">
              <ckeditor :editor="editor"
                        class="ck-content"
                        v-model="editorComment"
                        :config="editorConfig">
              </ckeditor>
              <b-button variant="dark"
                        @click="saveComment(post.id)"
                        :id="'button-comment' + post.id">
                Post
              </b-button>
            </div>
          </b-collapse>
          <div v-if="buttonsEngine['button-'+post.id].isOpen">
          </div>
        </div>
        <ckeditor :editor="editor"
                  class="ck-content"
                  v-model="editorPost"
                  :config="editorConfig">
        </ckeditor>
        <div class="button-control">
          <b-button @click="savePost" variant="dark">
            Post
          </b-button>
        </div>
      </div>
    </div>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="15"
      aria-controls="my-table"
    ></b-pagination>
  </div>
</template>

<script>
  import DeleteTopicButton from '../../SVG/DeleteTopicButton'
  import EditTopicButton from '../../SVG/EditTopicButton'
  import Profile from '../../SVG/Profile'
  import axios from 'axios'
  import {mapGetters} from 'vuex';
  import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

  export default {
    name: "Topic",
    data() {
      return {
        loading: false,
        topicID: this.$route.params.topicID,
        rows: 1,
        perPage: 3,
        topic: {
          title: "",
          description: "",
          body: "",
          totalLikes: 0,
          isLiked: false,
          removedByModerator: false,
          removedAt: null
        },
        author: {
          avatar: '',
          gameNickName: '',
          username: '',
          pk: 0
        },
        posts: [],
        buttonsEngine: {},
        editorPost: '',
        editorComment: '',
        editor: ClassicEditor,
        editorConfig: {},
        currentPage: 1,

      }
    },
    created() {
      this.getTopicData();
      this.getTopicPosts(this.currentPage)
    },
    components: {
      DeleteTopicButton,
      EditTopicButton,
      Profile,
    },
    watch: {
      '$route'(to, from) {
        this.getTopicData()
        this.getTopicPosts(this.currentPage);
      },
      'currentPage'() {
        this.getTopicPosts(this.currentPage);
      }
    },
    methods: {
      getTopicData() {
        return axios.get('topics/' + this.topicID + '/').then(
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
            this.removedByModerator = response.data.removed_by_moderator;
            this.removedAt = response.data.removed_at;
          }
        ).catch(
          (error) => {
            this.$router.push({name: 'home'})
          }
        )
      },
      profileClick(userID) {
        this.$router.push({
          name: 'user-profile',
          params: {
            id: userID
          }
        })
      },
      showDeleteModal() {
        this.$modal.show('deleteModal')
      },
      hideDeleteModal() {
        this.$modal.hide('deleteModal')
      },
      moderatorDeleteTopic() {
        const now = Math.floor(Date.now() / 1000)
        const data = {
          removed_by_moderator: true,
          removed_at: now,
        }
        axios.patch(`topics/${this.topicID}/`, data).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.hideDeleteModal()
            }
          }
        ).catch(
          (error) => {
            switch (error.response.status) {
              case 403:
                break
              default:
                break
            }
          }
        )
      },
      getTopicPosts(page) {
        this.loading = true
        axios.get('posts/', {
          params: {
            topic: this.topicID,
            page: page,
          }
        }).then((response) => {
          this.posts = response.data.results;
          this.rows = response.data.count
          this.posts.forEach(post => {
            let buttonID = 'button-' + post.id;
            this.$set(this.buttonsEngine, buttonID, {
              isOpen: false
            })
          })
          this.loading = false
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
          body: this.editorComment,
          post: postID
        };
        axios.post('comments/', data)
          .then((response) => {
            switch (response.status) {
              case 201:
                this.editorComment = '';
                this.getTopicPosts(this.currentPage);
                break;
              case 400:
                break
            }
          })
      },
      savePost() {
        const data = {
          body: this.editorPost,
          topic: this.topicID
        };
        axios.post('posts/', data)
          .then((response) => {
            switch (response.status) {
              case 201:
                this.editorPost = '';
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
          axios.post(`topics/${this.topicID}/unlike/`).then((response) => {
            switch (response.status) {
              case 200:
                this.getTopicData();
                break;
              case 400:
                break  // errors during serializing
            }
          })
        } else {
          axios.post(`topics/${this.topicID}/like/`).then((response) => {
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
        'getUserData',
        'isModerator',
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

  .html-text {
    align-content: initial;
  }
</style>
