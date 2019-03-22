<template lang="pug">
  v-app
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  components: {
  },
  data() {
  },
  mounted: () => {
    axios.get('http://localhost:5000')
      .then(
        response => {
          console.log(response);
        },
      );
  },
};
</script>
