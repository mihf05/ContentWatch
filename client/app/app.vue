<script setup>
useSeoMeta({
    title: "ContentWatch - AI-Driven Creator Intelligence",
    titleTemplate: (title) => title ? `${title} | ContentWatch` : "ContentWatch",

    description: "AI-Driven Creator Intelligence that analyzes your audience's deepest engagement patterns to deliver precise, actionable content strategies.",

    ogTitle: "ContentWatch",
    ogDescription: "AI-Driven Creator Intelligence that analyzes your audience's deepest engagement patterns to deliver precise, actionable content strategies.",

    ogType: "website",
    ogSiteName: "ContentWatch",

    twitterTitle: "ContentWatch",
    twitterDescription: "AI-Driven Creator Intelligence that analyzes your audience's deepest engagement patterns to deliver precise, actionable content strategies.",
    twitterCard: "summary_large_image",
})

useHead({
    htmlAttrs: {
        lang: "en",
        class: "dark"
    }
})
</script>

<template>
    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>
</template>