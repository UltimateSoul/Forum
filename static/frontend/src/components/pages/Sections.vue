<template>
  <div>
    <div class="row">
      <div class="col-lg-6">
        <div class="card bg-light mb-3 clicable" style="max-width: 18rem;"
        @click="sectionClick('ideas')">
          <div class="card-header">Ideas</div>
          <div class="card-body">
            <h5 class="card-title">Ideas forum section</h5>
            <p class="card-text">Here you can show your creativity and imagination</p>
          </div>
        </div>
      </div>
      <div class="col-lg-6">
        <div class="card bg-light mb-3 clicable" style="max-width: 18rem;"
        @click="sectionClick('bugs')">
          <div class="card-header clicable">Bugs</div>
          <div class="card-body">
            <h5 class="card-title">Bugs forum section</h5>
            <p class="card-text">Here you can share game issues with developers</p>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-6">
        <div class="card bg-light mb-3 clicable" style="max-width: 18rem;"
        @click="sectionClick('conversation')">
          <div class="card-header">Conversation</div>
          <div class="card-body">
            <h5 class="card-title">Conversation forum section</h5>
            <p class="card-text">Here you can communicate with other players</p>
          </div>
        </div>
      </div>
      <div class="col-lg-6">
        <div class="card bg-light mb-3 clicable" style="max-width: 18rem;"
        @click="sectionClick('entertainment')">
          <div class="card-header">Entertainment</div>
          <div class="card-body">
            <h5 class="card-title">Entertainment forum section</h5>
            <p class="card-text">Here you can just have fun and chill</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Sections",
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
 .clicable {
   cursor: pointer;
 }
</style>
