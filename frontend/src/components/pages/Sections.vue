<template>
  <div>
    <div class="sections-container">
      <div class="row">
        <div class="col-lg-6">
          <div class="card bg-light mb-3 clickable" style="max-width: 18rem;"
               @click="sectionClick('ideas')">
            <div class="card-body">
              <ideas-svg></ideas-svg>
              <h5 class="card-title">Ideas forum section</h5>
              <p class="card-text">Here you can show your creativity and imagination</p>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card bg-light mb-3 clickable" style="max-width: 18rem;"
               @click="sectionClick('bugs')">
            <div class="card-body">
              <bugs-svg></bugs-svg>
              <h5 class="card-title">Bugs forum section</h5>
              <p class="card-text">Here you can share game issues with developers</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-6">
          <div class="card bg-light mb-3 clickable" style="max-width: 18rem;"
               @click="sectionClick('conversation')">
            <div class="card-body">
              <conversation-svg></conversation-svg>
              <h5 class="card-title">Conversation forum section</h5>
              <p class="card-text">Here you can communicate with other players</p>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card bg-light mb-3 clickable" style="max-width: 18rem;"
               @click="sectionClick('entertainment')">
            <div class="card-body">
              <entertainment-svg></entertainment-svg>
              <h5 class="card-title">Entertainment forum section</h5>
              <p class="card-text">Here you can just have fun and chill</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import IdeasSvg from '../SVG/Ideas'
  import BugsSvg from '../SVG/Bugs'
  import ConversationSvg from '../SVG/Conversation'
  import EntertainmentSvg from '../SVG/Entertainment'

  export default {
    name: "Sections",
    components: {
      bugsSvg: BugsSvg,
      ideasSvg: IdeasSvg,
      conversationSvg: ConversationSvg,
      entertainmentSvg: EntertainmentSvg
    },
    methods: {
      sectionClick(section) {
        this.$router.push({
          name: 'conversation',
          params: {
            section: section
          }
        })
      }
    }
  }
</script>

<style scoped>
  .sections-container {
    margin: auto;
    width: 85%;
  }
</style>
