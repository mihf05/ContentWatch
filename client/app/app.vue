<script setup>
useSeoMeta({
    title: "Project Name",
    titleTemplate: (title) => title ? `${title} | Project Name` : "Project Name",

    description: "",

    ogTitle: "Project Name",
    ogDescription: "",

    ogType: "website",
    ogSiteName: "Project Name",

    twitterTitle: "Project Name",
    twitterDescription: "",
    twitterCard: "summary_large_image",
})

useHead({
    htmlAttrs: {
        lang: "en"
    }
})
</script>

<template>
    <UApp>
        <NuxtLayout>
            <NuxtPage />
        </NuxtLayout>
    </UApp>
</template>