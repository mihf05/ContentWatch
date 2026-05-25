<script setup>
const { popups, removePopup } = usePopup()
</script>

<template>
    <TransitionGroup name="toast" tag="div" class="fixed top-10 right-6 flex flex-col gap-3 z-50">
        <div v-for="popup in popups" :key="popup.id"
            class="w-[320px] px-4 py-3 rounded-xl border flex justify-between items-center gap-3 backdrop-blur-md shadow-2xl"
            :class="[
                popup.type === 'success'
                    ? 'bg-[#111111]/90 border-brand/20 text-white'
                    : 'bg-[#111111]/90 border-red-500/20 text-white'
            ]">

            <!-- Icon -->
            <span class="material-symbols-outlined shrink-0 mt-0.5"
                :class="popup.type === 'success' ? 'text-brand' : 'text-red-400'">
                {{ popup.type === 'success' ? 'check_circle' : 'error' }}
            </span>

            <!-- Message -->
            <span class="flex-1 text-sm font-medium leading-snug">{{ popup.message }}</span>

            <!-- Close btn -->
            <button @click="removePopup(popup.id)"
                class="shrink-0 text-gray-500 hover:text-white transition-colors cursor-pointer" aria-label="Close">
                <span class="material-symbols-outlined text-lg">close</span>
            </button>
        </div>
    </TransitionGroup>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
    opacity: 0;
    transform: translateX(40px) scale(0.95);
}

.toast-leave-to {
    opacity: 0;
    transform: translateX(40px) scale(0.95);
}

.toast-move {
    transition: transform 0.3s ease;
}
</style>