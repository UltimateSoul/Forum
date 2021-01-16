<template>
  <div>
    <ckeditor :editor="editor"
              class="ck-content"
              @input="updateData"
              v-model="data"
              :config="editorConfig"></ckeditor>
  </div>
</template>

<script>
  // import MyCustomUploadAdapterPlugin from '@/plugins/editor-image-upload'
  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';


  // ClassicEditor
  // .create( document.querySelector( '#editor' ), {
  //     extraPlugins: [ MyCustomUploadAdapterPlugin ],
  //
  //     // ...
  // } )
  // .catch( error => {
  //     console.log( error );
  // } );  // ToDo: resolve issues with uploading images

  export default {
    name: 'editor',
    props: ['editorData'],
    data() {
      return {
        editor: ClassicEditor,
        data: this.loadedText,
        editorConfig: {}
      };
    },
    methods: {
      updateData() {
        this.$emit('update', this.data)
      }
    },
    computed: {
      loadedText() {
        return this.editorData
      }
    }
  };
</script>
<style>

</style>
