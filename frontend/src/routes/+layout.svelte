<script lang="ts">
    import { page } from '$app/stores';
    
    const navItems = [
        { href: '/', label: 'Dashboard', icon: '🌍' },
        { href: '/about', label: 'About', icon: 'ℹ️' },
        { href: '/learn', label: 'Learn', icon: '📚' },
        { href: '/privacy', label: 'Privacy', icon: '🔒' }
    ];

    // Handle page metadata
    $: {
        if ($page.data?.title) {
            document.title = $page.data.title;
        } else {
            document.title = 'TerraPulse - Planetary Health Monitoring';
        }
        
        if ($page.data?.description) {
            updateMetaDescription($page.data.description);
        } else {
            updateMetaDescription('Real-time planetary health monitoring and environmental anomaly prediction');
        }
    }

    function updateMetaDescription(content: string) {
        let metaDescription = document.querySelector('meta[name="description"]');
        if (!metaDescription) {
            metaDescription = document.createElement('meta');
            (metaDescription as HTMLMetaElement).name = 'description';
            document.head.appendChild(metaDescription);
        }
        metaDescription.setAttribute('content', content);
    }
</script>

<nav class="navbar glass">
    <div class="nav-brand">
        <span class="logo">🌍</span>
        <span class="brand-text">TerraPulse</span>
    </div>
    
    <div class="nav-items">
        {#each navItems as item}
            <a 
                href={item.href} 
                class="nav-item {($page.url.pathname === item.href) ? 'active' : ''}"
            >
                <span class="nav-icon">{item.icon}</span>
                <span class="nav-label">{item.label}</span>
            </a>
        {/each}
    </div>
    
    <div class="nav-actions">
        <!-- Placeholder for future actions -->
    </div>
</nav>

<main>
    <slot />
</main>

<style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 20px;
        margin-bottom: 0;
        border-bottom: 1px solid var(--border-light);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .logo {
        font-size: 1.5rem;
    }
    
    .nav-items {
        display: flex;
        gap: 5px;
    }
    
    .nav-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 15px;
        border-radius: 8px;
        text-decoration: none;
        color: var(--text-secondary);
        transition: all 0.2s ease;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-primary);
    }
    
    .nav-item.active {
        background: rgba(139, 92, 246, 0.1);
        color: var(--accent-primary);
    }
    
    .nav-icon {
        font-size: 1.1rem;
    }
    
    .nav-label {
        font-weight: 500;
    }
    
    main {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    
    @media (max-width: 768px) {
        .nav-label {
            display: none;
        }
        
        .nav-item {
            padding: 10px;
        }
        
        .brand-text {
            display: none;
        }
    }
</style>