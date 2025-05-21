<template>
  <div class="user-avatar-wrapper">
    <img :src="avatarUrl" alt="User Avatar" class="avatar-image-standalone">
  </div>
</template>

<script>
import defaultAvatar from '@/assets/images/avatar.jpg';

export default {
  name: 'UserAvatar',
  data() {
    return {
      avatarUrl: defaultAvatar
    };
  }
}
</script>

<style scoped>
.user-avatar-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 20px rgba(230, 230, 255, 0.4),
              0 4px 8px rgba(0, 0, 0, 0.28);
}

.avatar-image-standalone {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>