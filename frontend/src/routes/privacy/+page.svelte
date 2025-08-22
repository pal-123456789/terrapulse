<script lang="ts">
  // This line receives the data object returned from the `load` function
  // in your +page.ts file.
  export let data;
</script>

<!-- 
  FIX: This is the correct SvelteKit way to set the page title and meta tags.
  It uses the `data` prop from the `load` function.
-->
<svelte:head>
    <title>{data.title}</title>
    <meta name="description" content={data.description} />
</svelte:head>

<div class="page-container">
    <div class="glass card">
        <div class="card-header">
            <h1>Privacy Policy</h1>
            <p class="subtitle">Last updated: {new Date().toLocaleDateString()}</p>
        </div>
        
        <div class="card-content">
            <h2>Data Collection and Usage</h2>
            <p>
                TerraPulse is committed to protecting your privacy. This policy explains how we collect,
                use, and protect your information when you use our services.
            </p>
            
            <h3>Information We Collect</h3>
            <ul>
                <li>
                    <strong>Environmental Data:</strong> We collect and process environmental data from various
                    sources including NASA satellites, weather services, and other public data providers.
                </li>
                <li>
                    <strong>Usage Data:</strong> We may collect information about how you interact with our
                    platform to improve our services.
                </li>
                <li>
                    <strong>Location Data:</strong> With your permission, we may access your approximate location
                    to provide relevant environmental alerts and information.
                </li>
            </ul>
            
            <h3>How We Use Your Information</h3>
            <ul>
                <li>To provide and maintain our services</li>
                <li>To notify you about environmental events and predictions</li>
                <li>To improve, personalize, and expand our services</li>
                <li>To develop new products, services, features, and functionality</li>
            </ul>
            
            <h3>Data Security</h3>
            <p>
                We implement appropriate technical and organizational measures to protect your personal
                information against unauthorized or unlawful processing, accidental loss, destruction, or damage.
            </p>
            
            <h3>Contact Us</h3>
            <p>
                If you have any questions about this Privacy Policy, please contact us at:
                <a href="mailto:privacy@terrapulse.com">privacy@terrapulse.com</a>
            </p>
        </div>
    </div>
</div>

<style>
    .page-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    h2 {
        margin: 25px 0 15px 0;
        color: var(--accent-primary);
    }
    h3 {
        margin: 20px 0 12px 0;
    }
    ul {
        padding-left: 20px;
        margin: 15px 0;
    }
    li {
        margin-bottom: 8px;
        line-height: 1.6;
    }
    strong {
        color: var(--accent-secondary);
    }
    a {
        color: var(--accent-primary);
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
