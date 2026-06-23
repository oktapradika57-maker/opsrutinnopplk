<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PT Kinarya Utama Teknik - Regional Kalimantan Enterprise Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
        }
        /* Custom Smooth Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 20px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        
        /* 3D Glassmorphism & Depth Utilities */
        .premium-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .premium-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px -10px rgba(79, 70, 229, 0.15), 0 1px 5px rgba(0, 0, 0, 0.03);
        }
        .active-menu-3d {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
            color: white !important;
            box-shadow: 0 8px 20px -4px rgba(79, 70, 229, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2);
            transform: translateX(6px);
        }
        .filter-select {
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1em;
        }

        /* Smooth View Transition Animation */
        .view-pane {
            animation: fadeInPage 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
        @keyframes fadeInPage {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Pulsing Glow Animation for Splash Screen */
        .logo-glow {
            animation: logoPulse 2s infinite ease-in-out;
        }
        @keyframes logoPulse {
            0%, 100% { transform: scale(1); filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.3)); }
            50% { transform: scale(1.03); filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.6)); }
        }
    </style>
</head>
<body class="bg-[#f8fafc] text-slate-800 overflow-hidden h-screen flex">

    <div id="splash-screen" class="fixed inset-0 bg-slate-950 z-50 flex flex-col items-center justify-center transition-opacity duration-700 ease-in-out">
        <div class="text-center space-y-6 max-w-md px-6">
            <div class="logo-glow bg-white p-6 rounded-2xl inline-block shadow-[0_20px_50px_rgba(79,70,229,0.3)] border border-slate-800">
                <div class="flex flex-col items-center justify-center">
                    <i class="fa-solid fa-network-wired text-5xl text-indigo-600 mb-2"></i>
                    <span class="text-xl font-black text-slate-900 tracking-tight">KUT SYSTEM</span>
                </div>
            </div>
            
            <div class="space-y-2">
                <h2 class="text-white text-xl font-extrabold tracking-wide">PT KINARYA UTAMA TEKNIK</h2>
                <p class="text-indigo-400 text-xs font-bold uppercase tracking-widest">Regional Kalimantan Dashboard</p>
            </div>

            <div class="w-48 h-1.5 bg-slate-900 rounded-full mx-auto overflow-hidden relative">
                <div class="h-full bg-gradient-to-r from-indigo-500 to-purple-600 w-full rounded-full absolute -translateX-full animate-[loadingBar_2s_infinite_ease-in-out]"></div>
            </div>
            <p class="text-slate-500 text-[11px] font-medium tracking-wider">Menghubungkan ke Database Live Spreadsheet...</p>
        </div>
    </div>
    
    <style>
        @keyframes loadingBar {
            0% { left: -100%; right: 100%; }
            50% { left: 0%; right: 0%; }
            100% { left: 100%; right: -100%; }
        }
    </style>

    <aside id="sidebar" class="w-68 bg-slate-950 text-slate-400 flex flex-col h-full flex-shrink-0 shadow-[4px_0_25px_rgba(0,0,0,0.15)] z-20 border-r border-slate-900 transition-all duration-300 overflow-hidden">
        <div class="p-6 flex items-center space-x-3.5 border-b border-slate-900 bg-slate-950 whitespace-nowrap">
            <div class="bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 rounded-xl text-white shadow-[0_4px_12px_rgba(79,70,229,0.5)]">
                <i class="fa-solid fa-chart-pie text-xl w-6 text-center"></i>
            </div>
            <div>
                <h1 class="text-white font-extrabold text-sm tracking-wider leading-tight">REGIONAL KAL</h1>
                <p class="text-[11px] text-indigo-400 font-bold uppercase tracking-widest">PT KUT Enterprise Base</p>
            </div>
        </div>

        <nav class="flex-1 overflow-y-auto p-4 space-y-2.5 text-sm whitespace-nowrap">
            <button onclick="toggleSection('main-analyzer-container', 'arrow-main-analyzer')" class="w-full flex items-center justify-between px-3 py-2 text-[10px] font-bold text-slate-500 hover:text-indigo-400 uppercase tracking-widest transition-colors duration-200 group focus:outline-none">
                <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-layer-group text-slate-600 group-hover:text-indigo-400"></i>
                    <span>Main Analyzer</span>
                </div>
                <i id="arrow-main-analyzer" class="fa-solid fa-chevron-down text-xs transition-transform duration-300"></i>
            </button>
            
            <div id="main-analyzer-container" class="space-y-2.5 transition-all duration-300">
                <a href="#excel-analyzer" id="btn-excel-analyzer" class="menu-btn w-full flex items-center justify-between px-4 py-3 rounded-xl font-semibold transition-all duration-300 hover:bg-slate-900 hover:text-white group">
                    <div class="flex items-center space-x-3.5">
                        <i class="fa-solid fa-file-excel text-lg w-5 text-center text-slate-500 group-hover:text-emerald-400 group-hover:scale-110 transition-all duration-300"></i>
                        <span>Analisa Drop Excel</span>
                    </div>
                    <i class="fa-solid fa-chevron-right text-[10px] opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-300"></i>
                </a>

                <a href="#sva" id="btn-sva" class="menu-btn w-full flex items-center justify-between px-4 py-3 rounded-xl font-semibold transition-all duration-300 hover:bg-slate-900 hover:text-white group">
                    <div class="flex items-center space-x-3.5">
                        <i class="fa-solid fa-wallet text-lg w-5 text-center text-slate-500 group-hover:text-indigo-400 group-hover:scale-110 transition-all duration-300"></i>
                        <span>Monitoring SVA (Profit)</span>
                    </div>
                    <i class="fa-solid fa-chevron-right text-[10px] opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-300"></i>
                </a>

                <div class="space-y-1">
                    <button onclick="toggleSubmenu('submenu-pm')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl font-semibold transition-all duration-300 hover:bg-slate-900 hover:text-white group">
                        <div class="flex items-center space-x-3.5">
                            <i class="fa-solid fa-screwdriver-wrench text-lg w-5 text-center text-slate-500 group-hover:text-indigo-400 group-hover:scale-110 transition-all duration-300"></i>
                            <span>Monitoring PM</span>
                        </div>
                        <i id="arrow-submenu-pm" class="fa-solid fa-chevron-down text-xs transition-transform duration-300"></i>
                    </button>
                    <div id="submenu-pm" class="pl-6 space-y-1 bg-slate-900/30 py-1.5 rounded-xl border-l-2 border-slate-800 ml-4 hidden transition-all duration-300">
                        <a href="#pm-target" id="btn-pm-target" class="menu-btn w-full text-left px-4 py-2.5 text-xs font-medium rounded-lg text-slate-400 hover:text-white block hover:translate-x-1 transition-all duration-300"><i class="fa-solid fa-bullseye mr-2 text-[10px] text-slate-600"></i>Target & Pencapaian</a>
                        <a href="#pm-curvas" id="btn-pm-curvas" class="menu-btn w-full text-left px-4 py-2.5 text-xs font-medium rounded-lg text-slate-400 hover:text-white block hover:translate-x-1 transition-all duration-300"><i class="fa-solid fa-chart-line mr-2 text-[10px] text-slate-600"></i>Curva S Progress</a>
                    </div>
                </div>

                <div class="space-y-1">
                    <button onclick="toggleSubmenu('submenu-mbp')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl font-semibold transition-all duration-300 hover:bg-slate-900 hover:text-white group">
                        <div class="flex items-center space-x-3.5">
                            <i class="fa-solid fa-gas-pump text-lg w-5 text-center text-slate-500 group-hover:text-indigo-400 group-hover:scale-110 transition-all duration-300"></i>
                            <span>Monitoring MBP</span>
                        </div>
                        <i id="arrow-submenu-mbp" class="fa-solid fa-chevron-down text-xs transition-transform duration-300"></i>
                    </button>
                    <div id="submenu-mbp" class="pl-6 space-y-1 bg-slate-900/30 py-1.5 rounded-xl border-l-2 border-slate-800 ml-4 hidden transition-all duration-300">
                        <a href="#mbp-rh" id="btn-mbp-rh" class="menu-btn w-full text-left px-4 py-2.5 text-xs font-medium rounded-lg text-slate-400 hover:text-white block hover:translate-x-1 transition-all duration-300"><i class="fa-solid fa-hourglass-half mr-2 text-[10px] text-slate-600"></i>Perhitungan Total RH</a>
                        <a href="#mbp-bbm" id="btn-mbp-bbm" class="menu-btn w-full text-left px-4 py-2.5 text-xs font-medium rounded-lg text-slate-400 hover:text-white block hover:translate-x-1 transition-all duration-300"><i class="fa-solid fa-droplet mr-2 text-[10px] text-slate-600"></i>Analisa Konsumsi BBM</a>
                    </div>
                </div>

                <div class="space-y-1">
                    <button onclick="toggleSubmenu('submenu-asset')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl font-semibold transition-all duration-300 hover:bg-slate-900 hover:text-white group">
                        <div class="flex items-center space-x-3.5">
                            <i class="fa-solid fa-car text-lg w-5 text-center text-slate-500 group-hover:text-indigo-400 group-hover:scale-110 transition-all duration-300"></i>
                            <span>Asset KUT System</span>
                        </div>
                        <i id="arrow-submenu-asset" class="fa-solid fa-chevron-down text-xs transition-transform duration-300"></i>
                    </button>
                    <div id="submenu-asset" class="pl-6 space-y-1 bg-slate-900/30 py-1.5 rounded-xl border-l-2 border-slate-800 ml-4 hidden transition-all duration-300">
                        <a href="#asset-service" id="btn-asset-service" class="menu-btn w-full text-left px-4 py-2.5 text-xs font-medium rounded-lg text-slate-400 hover:text-white block hover:translate-x-1 transition-all duration-300"><i class="fa-solid fa-wrench mr-2 text-[10px] text-slate-600"></i>Biaya Perawatan Service</a>
                        <a href="#asset-depresiasi" id="btn-asset-depresiasi" class="menu-btn w-full text-left px-4 py-2.5 text-xs font-medium rounded-lg text-slate-400 hover:text-white block hover:translate-x-1 transition-all duration-300"><i class="fa-solid fa-arrow-down-line mr-2 text-[10px] text-slate-600"></i>Depresiasi Nilai Buku</a>
                        <a href="#asset-sewa" id="btn-asset-sewa" class="menu-btn w-full text-left px-4 py-2.5 text-xs font-medium rounded-lg text-slate-400 hover:text-white block hover:translate-x-1 transition-all duration-300"><i class="fa-solid fa-handshake mr-2 text-[10px] text-slate-600"></i>Biaya Sewa Vendor</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="p-4 border-t border-slate-900 bg-slate-950 text-xs flex items-center justify-between whitespace-nowrap">
            <span class="text-slate-500 font-medium">Data State:</span>
            <span id="data-status-badge" class="px-2.5 py-1 bg-amber-500/10 text-amber-400 rounded-lg text-[10px] font-bold tracking-wider uppercase border border-amber-500/20 shadow-md">Syncing</span>
        </div>
    </aside>

    <main class="flex-1 flex flex-col h-full overflow-hidden">
        
        <header class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200/80 px-8 flex items-center justify-between flex-shrink-0 z-10 shadow-[0_2px_15px_rgba(0,0,0,0.02)]">
            <div class="flex items-center space-x-2.5">
                <button onclick="toggleSidebar()" class="mr-2 text-slate-600 hover:text-indigo-600 p-2 rounded-xl hover:bg-slate-100 transition-all focus:outline-none" title="Sembunyikan/Tampilkan Menu">
                    <i id="sidebar-toggle-icon" class="fa-solid fa-bars text-lg"></i>
                </button>
                <span class="text-slate-400 text-xs font-semibold uppercase tracking-wider">PT KUT Portal</span>
                <span class="text-slate-300 text-sm">/</span>
                <span id="breadcrumb-current" class="text-slate-900 font-bold text-base tracking-tight">Monitoring SVA</span>
            </div>
            
            <div class="flex items-center space-x-5">
                <button onclick="reloadData()" class="px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold rounded-xl flex items-center space-x-2 transition-all shadow-[0_4px_10px_rgba(79,70,229,0.06)] active:scale-95">
                    <i id="sync-icon" class="fa-solid fa-arrows-rotate"></i>
                    <span>Sinkronisasi Live Data</span>
                </button>
                <div class="h-6 w-px bg-slate-200"></div>
                <div class="flex items-center space-x-3">
                    <div class="text-right">
                        <p class="text-xs font-bold text-slate-800 leading-tight">Financial Operator</p>
                        <p class="text-[10px] text-indigo-500 font-bold uppercase tracking-wider">Kalimantan Center</p>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-slate-200 to-slate-300 flex items-center justify-between p-2.5 text-slate-600 font-bold shadow-inner">
                        <i class="fa-solid fa-user-tie text-lg"></i>
                    </div>
                </div>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto p-8 space-y-8" id="dashboard-content">
            
            <section id="view-excel-analyzer" class="view-pane space-y-8 hidden">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    
                    <div class="space-y-6 flex flex-col">
                        <div id="drop-zone" class="premium-card p-10 rounded-2xl border-2 border-dashed border-slate-300 hover:border-indigo-500 bg-white text-center cursor-pointer transition-all flex flex-col items-center justify-center space-y-4">
                            <div class="bg-emerald-50 text-emerald-600 p-4 rounded-full">
                                <i class="fa-solid fa-cloud-arrow-up text-3xl"></i>
                            </div>
                            <div>
                                <p class="text-sm font-bold text-slate-800">Tarik & Lepas File Excel Anda Di Sini</p>
                                <p class="text-xs text-slate-400 mt-1">Mendukung format berkas .xlsx, .xls, atau .csv</p>
                            </div>
                            <input type="file" id="excel-file-input" class="hidden" accept=".xlsx, .xls, .csv">
                            <div id="file-info-zone" class="hidden text-xs bg-emerald-50 border border-emerald-200 text-emerald-700 px-3 py-1.5 rounded-xl font-semibold"></div>
                        </div>
                        
                        <div class="premium-card p-6 rounded-2xl bg-white flex-1 flex flex-col">
                            <h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-4"><i class="fa-solid fa-brain mr-2 text-indigo-500"></i>Kalkulasi & Kesimpulan Analisa Otomatis</h4>
                            <div id="excel-analysis-text" class="text-xs text-slate-500 space-y-3 leading-relaxed flex-1 flex items-center justify-center text-center italic">
                                Silakan jatuhkan berkas Excel Anda di atas untuk memproses komparasi pendapatan versus pengeluaran perusahaan secara langsung.
                            </div>
                        </div>
                    </div>

                    <div class="premium-card p-6 rounded-2xl bg-white flex flex-col min-h-[480px]">
                        <h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-chart-bar mr-2 text-indigo-500"></i>Visualisasi Komparasi Pengeluaran vs Pendapatan</h4>
                        <div class="w-full flex-1 relative flex items-center justify-center">
                            <canvas id="chart-excel-comparison"></canvas>
                            <div id="chart-empty-state" class="absolute inset-0 flex items-center justify-center text-xs italic text-slate-400 bg-white/50">Grafik komparasi akan dimuat otomatis saat file Excel dibaca.</div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="view-sva" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Analisa Keuangan</span></div>
                    <select id="filter-sva-bulan" onchange="applyFilters()" class="filter-select w-48 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Total Gross Revenue</p><h3 id="sva-kpi-1" class="text-2xl font-extrabold text-slate-900 mt-2">Rp 0</h3></div><div class="bg-blue-50 p-3.5 rounded-xl text-blue-600"><i class="fa-solid fa-money-bill-trend-up text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Total Laba Kotor</p><h3 id="sva-kpi-2" class="text-2xl font-extrabold text-amber-600 mt-2">Rp 0</h3></div><div class="bg-amber-50 p-3.5 rounded-xl text-amber-600"><i class="fa-solid fa-sack-dollar text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Total Laba Bersih</p><h3 id="sva-kpi-3" class="text-2xl font-extrabold text-emerald-600 mt-2">Rp 0</h3></div><div class="bg-emerald-50 p-3.5 rounded-xl text-emerald-600"><i class="fa-solid fa-building-columns text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Net Profit Margin</p><h3 id="sva-kpi-4" class="text-2xl font-extrabold text-indigo-600 mt-2">0%</h3></div><div class="bg-indigo-50 p-3.5 rounded-xl text-indigo-600"><i class="fa-solid fa-percent text-xl"></i></div></div>
                </div>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div class="premium-card p-6 rounded-2xl lg:col-span-2"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-chart-line mr-2 text-indigo-500"></i>Tren Skala Finansial SVA Bulanan</h4><div class="w-full h-80"><canvas id="chart-sva-finance-line"></canvas></div></div>
                    <div class="premium-card p-6 rounded-2xl lg:col-span-1"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-4"><i class="fa-solid fa-chart-pie mr-2 text-indigo-500"></i>Proporsi Struktur Alokasi</h4><div class="relative w-full h-72 flex items-center justify-center"><canvas id="chart-sva-finance-pie"></canvas></div></div>
                </div>
                <div class="premium-card rounded-2xl overflow-hidden border border-slate-200">
                    <div class="px-6 py-5 border-b border-slate-100 bg-slate-50/50"><h4 class="text-xs font-extrabold text-slate-700 uppercase tracking-widest">Laporan Neraca Analisa SVA</h4></div>
                    <div class="overflow-x-auto"><table class="w-full text-left border-collapse text-xs" id="table-sva"></table></div>
                </div>
            </section>

            <section id="view-pm-target" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Bulanan Target WO</span></div>
                    <select id="filter-pm-target-bulan" onchange="applyFilters()" class="filter-select w-48 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Target Bulanan</p><h3 id="pmt-kpi-1" class="text-2xl font-extrabold text-slate-800 mt-2">0 WO</h3></div><div class="bg-blue-50 p-3.5 rounded-xl text-blue-600 shadow-md"><i class="fa-solid fa-bullseye text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Pencapaian Realisasi</p><h3 id="pmt-kpi-2" class="text-2xl font-extrabold text-emerald-600 mt-2">0 WO</h3></div><div class="bg-emerald-50 p-3.5 rounded-xl text-emerald-600 shadow-md"><i class="fa-solid fa-circle-check text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Sisa Deviasi Sifat</p><h3 id="pmt-kpi-3" class="text-2xl font-extrabold text-rose-600 mt-2">0 WO</h3></div><div class="bg-rose-50 p-3.5 rounded-xl text-rose-600 shadow-md"><i class="fa-solid fa-triangle-exclamation text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">% Pencapaian</p><h3 id="pmt-kpi-4" class="text-2xl font-extrabold text-indigo-600 mt-2">0%</h3></div><div class="bg-indigo-50 p-3.5 rounded-xl text-indigo-600 shadow-md"><i class="fa-solid fa-chart-line text-xl"></i></div></div>
                </div>
                <div class="premium-card p-6 rounded-2xl"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-chart-bar mr-2 text-indigo-500"></i>Visualisasi Matriks Komparatif PM Target</h4><div class="w-full h-80"><canvas id="chart-pm-target"></canvas></div></div>
                <div class="premium-card rounded-2xl overflow-hidden"><div class="overflow-x-auto"><table class="w-full text-left border-collapse text-xs" id="table-pm-target"></table></div></div>
            </section>

            <section id="view-pm-curvas" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Skala Minggu Progress</span></div>
                    <select id="filter-pm-curvas-minggu" onchange="applyFilters()" class="filter-select w-48 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="premium-card p-6 rounded-2xl"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-chart-area mr-2 text-emerald-500"></i>S-Curve Kumulatif Progress Proyek Pemeliharaan</h4><div class="w-full h-[420px]"><canvas id="chart-pm-curvas"></canvas></div></div>
            </section>

            <section id="view-mbp-rh" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Unit Genset Aktif</span></div>
                    <select id="filter-mbp-rh-unit" onchange="applyFilters()" class="filter-select w-52 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Accumulated Running Hours</p><h3 id="mbprh-kpi-1" class="text-2xl font-extrabold text-slate-800 mt-2">0 Jam</h3></div><div class="bg-slate-100 p-3.5 rounded-xl text-slate-700"><i class="fa-solid fa-hourglass-high text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Rata-Rata Delta RH Mesin</p><h3 id="mbprh-kpi-2" class="text-2xl font-extrabold text-indigo-600 mt-2">0 Jam</h3></div><div class="bg-indigo-50 p-3.5 rounded-xl text-indigo-600"><i class="fa-solid fa-bolt text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Total Durasi Kerja (Delta Time)</p><h3 id="mbprh-kpi-3" class="text-2xl font-extrabold text-teal-600 mt-2">0 Jam</h3></div><div class="bg-teal-50 p-3.5 rounded-xl text-teal-600"><i class="fa-solid fa-clock text-xl"></i></div></div>
                </div>
                <div class="premium-card p-6 rounded-2xl"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-clock-rotate-left mr-2 text-cyan-500"></i>Analisis Log Delta Running Hours Beban Kerja Sistem</h4><div class="w-full h-80"><canvas id="chart-mbp-rh"></canvas></div></div>
                <div class="premium-card rounded-2xl overflow-hidden"><div class="overflow-x-auto"><table class="w-full text-left border-collapse text-xs" id="table-mbp-rh"></table></div></div>
            </section>

            <section id="view-mbp-bbm" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Unit Distribusi BBM</span></div>
                    <select id="filter-mbp-bbm-unit" onchange="applyFilters()" class="filter-select w-52 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Akumulasi Konsumsi Solar</p><h3 id="mbpbbm-kpi-1" class="text-2xl font-extrabold text-amber-600 mt-2">0 Liter</h3></div><div class="bg-amber-50 p-3.5 rounded-xl text-amber-600"><i class="fa-solid fa-gas-pump text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Rasio Efisiensi Bahan Bakar</p><h3 id="mbpbbm-kpi-2" class="text-2xl font-extrabold text-indigo-600 mt-2">0 Ltr/Jam</h3></div><div class="bg-indigo-50 p-3.5 rounded-xl text-indigo-600"><i class="fa-solid fa-gauge-high text-xl"></i></div></div>
                    <div class="premium-card p-6 rounded-2xl flex items-center justify-between"><div><p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Status Integritas Mesin</p><h3 id="mbpbbm-kpi-3" class="text-2xl font-extrabold text-emerald-600 mt-2">Sangat Baik</h3></div><div class="bg-emerald-50 p-3.5 rounded-xl text-emerald-600"><i class="fa-solid fa-shield-heart text-xl"></i></div></div>
                </div>
                <div class="premium-card p-6 rounded-2xl"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-fill-drip mr-2 text-amber-500"></i>Korelasi Pengeluaran Liter BBM Terhadap Jam Delta RH</h4><div class="w-full h-80"><canvas id="chart-mbp-bbm"></canvas></div></div>
                <div class="premium-card rounded-2xl overflow-hidden"><div class="overflow-x-auto"><table class="w-full text-left border-collapse text-xs" id="table-mbp-bbm"></table></div></div>
            </section>

            <section id="view-asset-service" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Lokasi Aset Perawatan</span></div>
                    <select id="filter-asset-service-lokasi" onchange="applyFilters()" class="filter-select w-52 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="premium-card p-6 rounded-2xl"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-screwdriver-wrench mr-2 text-pink-500"></i>Grafik Log Alokasi Pendanaan Perawatan Kendaraan & Genset KUT</h4><div class="w-full h-80"><canvas id="chart-asset-service"></canvas></div></div>
                <div class="premium-card rounded-2xl overflow-hidden"><div class="overflow-x-auto"><table class="w-full text-left border-collapse text-xs" id="table-asset-service"></table></div></div>
            </section>

            <section id="view-asset-depresiasi" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Kategori Depresiasi</span></div>
                    <select id="filter-asset-depresiasi-kat" onchange="applyFilters()" class="filter-select w-52 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="premium-card p-6 rounded-2xl"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-calculator mr-2 text-purple-500"></i>Garis Penyusutan Nilai Buku Aset Inventaris Regional</h4><div class="w-full h-80"><canvas id="chart-asset-depresiasi"></canvas></div></div>
                <div class="premium-card rounded-2xl overflow-hidden"><div class="overflow-x-auto"><table class="w-full text-left border-collapse text-xs" id="table-asset-depresiasi"></table></div></div>
            </section>

            <section id="view-asset-sewa" class="view-pane space-y-8 hidden">
                <div class="premium-card p-4 rounded-xl flex items-center justify-between bg-white">
                    <div class="flex items-center space-x-2 text-indigo-600"><i class="fa-solid fa-filter text-sm"></i><span class="text-xs font-bold uppercase tracking-wider">Filter Wilayah Sewa Vendor</span></div>
                    <select id="filter-asset-sewa-lokasi" onchange="applyFilters()" class="filter-select w-52 bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                </div>
                <div class="premium-card p-6 rounded-2xl"><h4 class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-6"><i class="fa-solid fa-building-user mr-2 text-blue-500"></i>Biaya Sewa Vendor Penyokong Unit Logistik</h4><div class="w-full h-80"><canvas id="chart-asset-sewa"></canvas></div></div>
                <div class="premium-card rounded-2xl overflow-hidden"><div class="overflow-x-auto"><table class="w-full text-left border-collapse text-xs" id="table-asset-sewa"></table></div></div>
            </section>

        </div>
    </main>

    <script>
        const SPREADSHEET_ID = '1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw';
        let charts = {};
        let currentView = 'sva';
        let globalDataset = {};

        const CONFIG_SHEETS = {
            'sva': 'data SVA',
            'pm-target': 'PM_Target',
            'pm-curvas': 'PM_CurvaS',
            'mbp-rh': 'MBP_RH',
            'mbp-bbm': 'MBP_BBM',
            'asset-service': 'Asset_KUT'
        };

        const MOCK_DATA = {
            'sva': [
                { 'Bulan': 'Januari', 'Revenue': 165000000, 'Laba_Kotor': 105000000, 'Net_Income': 48000000 },
                { 'Bulan': 'Februari', 'Revenue': 198000000, 'Laba_Kotor': 125000000, 'Net_Income': 62000000 },
                { 'Bulan': 'Maret', 'Revenue': 172000000, 'Laba_Kotor': 102000000, 'Net_Income': 45000000 }
            ],
            'pm-target': [{ 'Bulan': 'Januari', 'Target_WO': 120, 'Realisasi_WO': 115 }],
            'pm-curvas': [{ 'Minggu': 'W1', 'Rencana_Kumulatif': 20, 'Aktual_Kumulatif': 18 }],
            'mbp-rh': [{ 'Unit_Genset': 'Genset KUT-01', 'Tanggal': '2026-06-20', 'RH_Awal': 1420, 'RH_Akhir': 1435, 'Delta_RH': 15, 'Delta_Time': 15 }],
            'mbp-bbm': [{ 'Tanggal': '2026-06-20', 'Unit': 'Genset KUT-01', 'Delta_RH': 15, 'Liter_BBM': 45, 'Rasio_Ltr_Jam': 3.0 }],
            'asset-kut': [{ 'ID_Asset': 'KUT-V-101', 'Nama_Aset': 'Trinton Operational 4x4', 'Kategori': 'Kendaraan', 'Biaya_Service': 5500000, 'Depresiasi': 2800000, 'Biaya_Sewa': 0, 'Lokasi': 'Balikpapan' }]
        };

        window.addEventListener('DOMContentLoaded', () => {
            window.addEventListener('hashchange', evaluateRoute);
            setupExcelDropZone();
            reloadData();
        });

        function evaluateRoute() {
            let hash = window.location.hash.replace('#', '') || 'sva';
            currentView = hash;

            document.querySelectorAll('.view-pane').forEach(el => el.classList.add('hidden'));
            
            let targetPane = currentView;
            const paneEl = document.getElementById(`view-${targetPane}`);
            if(paneEl) {
                paneEl.classList.remove('hidden');
            }

            document.querySelectorAll('.menu-btn').forEach(el => el.classList.remove('active-menu-3d'));
            const activeBtn = document.getElementById(`btn-${currentView}`);
            if(activeBtn) activeBtn.classList.add('active-menu-3d');

            const titleLabels = {
                'excel-analyzer': 'Analisa File Excel > Komparasi Pendapatan & Pengeluaran',
                'sva': 'Monitoring SVA (Analisa Kompetitif Pendapatan)',
                'pm-target': 'Monitoring PM > Analisa Target Kerja',
                'pm-curvas': 'Monitoring PM > S-Curve Progress',
                'mbp-rh': 'Monitoring MBP > Log Perhitungan Running Hours',
                'mbp-bbm': 'Monitoring MBP > Log Analisa Konsumsi BBM',
                'asset-service': 'Asset KUT System > Log Biaya Service',
                'asset-depresiasi': 'Asset KUT System > Penyusutan Nilai Buku',
                'asset-sewa': 'Asset KUT System > Pembiayaan Unit Sewa'
            };
            document.getElementById('breadcrumb-current').innerText = titleLabels[currentView] || 'Portal';

            if(Object.keys(globalDataset).length > 0) {
                renderActiveView(globalDataset);
            }
        }

        async function fetchFromSpreadsheet(sheetName) {
            const url = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/gviz/tq?tqx=out:json&sheet=${encodeURIComponent(sheetName)}`;
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error('Fail');
                const text = await response.text();
                const startIdx = text.indexOf('{');
                const endIdx = text.lastIndexOf('}');
                const rawJson = JSON.parse(text.substring(startIdx, endIdx + 1));
                const headers = rawJson.table.cols.map(col => col.label ? col.label.trim().replace(/ /g, '_') : '');
                
                return rawJson.table.rows.map(row => {
                    let obj = {};
                    row.c.forEach((cell, idx) => {
                        const key = headers[idx] || `Kolom_${idx}`;
                        obj[key] = cell ? cell.v : null;
                    });
                    return obj;
                });
            } catch (e) { return null; }
        }

        async function reloadData() {
            const syncIcon = document.getElementById('sync-icon');
            const badge = document.getElementById('data-status-badge');
            syncIcon.classList.add('fa-spin');
            badge.innerText = 'PROSES SYNC...';

            for (let key of Object.keys(CONFIG_SHEETS)) {
                let res = await fetchFromSpreadsheet(CONFIG_SHEETS[key]);
                globalDataset[key] = res || (key.startsWith('asset-') ? MOCK_DATA['asset-kut'] : MOCK_DATA[key]);
            }

            buildFilterOptions('filter-sva-bulan', globalDataset['sva'], 'Bulan', 'Semua Bulan');
            buildFilterOptions('filter-pm-target-bulan', globalDataset['pm-target'], 'Bulan', 'Semua Bulan');
            buildFilterOptions('filter-pm-curvas-minggu', globalDataset['pm-curvas'], 'Minggu', 'Semua Minggu');
            buildFilterOptions('filter-mbp-rh-unit', globalDataset['mbp-rh'], 'Unit_Genset', 'Semua Unit Genset');
            buildFilterOptions('filter-mbp-bbm-unit', globalDataset['mbp-bbm'], 'Unit', 'Semua Unit');
            buildFilterOptions('filter-asset-service-lokasi', globalDataset['asset-service'], 'Lokasi', 'Semua Wilayah');
            buildFilterOptions('filter-asset-depresiasi-kat', globalDataset['asset-service'], 'Kategori', 'Semua Kategori');
            buildFilterOptions('filter-asset-sewa-lokasi', globalDataset['asset-service'], 'Lokasi', 'Semua Lokasi Sewa');

            badge.innerText = 'LIVE ENTERPRISE';
            badge.className = "px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-lg text-[10px] font-bold tracking-wider uppercase border border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.2)]";
            syncIcon.classList.remove('fa-spin');

            const splash = document.getElementById('splash-screen');
            if(splash) {
                splash.classList.add('opacity-0', 'pointer-events-none');
                setTimeout(() => splash.remove(), 700);
            }

            if(!window.location.hash) window.location.hash = '#sva';
            else evaluateRoute();
        }

        function buildFilterOptions(selectId, dataArray, objectKey, defaultLabel) {
            const selectEl = document.getElementById(selectId);
            if(!selectEl) return;
            const uniqueValues = [...new Set(dataArray.map(item => item[objectKey]).filter(Boolean))];
            
            let html = `<option value="ALL">✨ ${defaultLabel}</option>`;
            uniqueValues.forEach(val => { html += `<option value="${val}">${val}</option>`; });
            selectEl.innerHTML = html;
        }

        function applyFilters() { renderActiveView(globalDataset); }

        function toggleSection(containerId, arrowId) {
            const container = document.getElementById(containerId);
            const arrow = document.getElementById(arrowId);
            if(container) container.classList.toggle('hidden');
            if(arrow) arrow.classList.toggle('rotate-180');
        }

        function toggleSubmenu(id) { toggleSection(id, `arrow-${id}`); }

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const icon = document.getElementById('sidebar-toggle-icon');
            if (sidebar.classList.contains('w-68')) {
                sidebar.classList.remove('w-68');
                sidebar.classList.add('w-0', 'border-r-0');
                icon.className = 'fa-solid fa-outdent text-lg';
            } else {
                sidebar.classList.remove('w-0', 'border-r-0');
                sidebar.classList.add('w-68');
                icon.className = 'fa-solid fa-bars text-lg';
            }
        }

        /* ENGINE LOGIC BARU: DRAG & DROP READER EXCEL */
        function setupExcelDropZone() {
            const dropZone = document.getElementById('drop-zone');
            const fileInput = document.getElementById('excel-file-input');
            if(!dropZone || !fileInput) return;

            dropZone.addEventListener('click', () => fileInput.click());
            dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('border-indigo-500', 'bg-indigo-50/20'); });
            dropZone.addEventListener('dragleave', () => { dropZone.classList.remove('border-indigo-500', 'bg-indigo-50/20'); });
            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('border-indigo-500', 'bg-indigo-50/20');
                if(e.dataTransfer.files.length) {
                    fileInput.files = e.dataTransfer.files;
                    processExcelFile(e.dataTransfer.files[0]);
                }
            });
            fileInput.addEventListener('change', (e) => {
                if(e.target.files.length) processExcelFile(e.target.files[0]);
            });
        }

        function processExcelFile(file) {
            const fileInfo = document.getElementById('file-info-zone');
            if(fileInfo) {
                fileInfo.classList.remove('hidden');
                fileInfo.innerText = `📄 ${file.name} (${(file.size/1024).toFixed(1)} KB)`;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, {type: 'array'});
                    const worksheet = workbook.Sheets[workbook.SheetNames[0]];
                    const json = XLSX.utils.sheet_to_json(worksheet);
                    analyzeExcelData(json);
                } catch(err) {
                    alert('Gagal membaca struktur berkas Excel. Gunakan dokumen tabel baris yang valid.');
                }
            };
            reader.readAsArrayBuffer(file);
        }

        function analyzeExcelData(json) {
            if(!json || json.length === 0) {
                alert('Tabel terdeteksi kosong.');
                return;
            }

            let labelKey = '', revenueKey = '', expenseKey = '';
            const sample = json[0];
            const keys = Object.keys(sample);

            keys.forEach(k => {
                const kl = k.toLowerCase();
                if(kl.includes('bulan') || kl.includes('month') || kl.includes('label') || kl.includes('kategori') || kl.includes('tanggal') || kl.includes('date')) labelKey = k;
                if(kl.includes('pendapatan') || kl.includes('revenue') || kl.includes('pemasukan') || kl.includes('omset') || kl.includes('income')) revenueKey = k;
                if(kl.includes('pengeluaran') || kl.includes('beban') || kl.includes('expense') || kl.includes('spending') || kl.includes('biaya')) expenseKey = k;
            });

            if(!labelKey) labelKey = keys[0];
            if(!revenueKey) revenueKey = keys[1] || keys[0];
            if(!expenseKey) expenseKey = keys[2] || keys[1] || keys[0];

            let labels = [], revenues = [], expenses = [];
            let totalRevenue = 0, totalExpense = 0;

            json.forEach((row, index) => {
                let lbl = row[labelKey] || `Baris ${index + 1}`;
                let rev = parseFloat(row[revenueKey]) || 0;
                let exp = parseFloat(row[expenseKey]) || 0;

                labels.push(lbl);
                revenues.push(rev);
                expenses.push(exp);
                totalRevenue += rev;
                totalExpense += exp;
            });

            const emptyState = document.getElementById('chart-empty-state');
            if(emptyState) emptyState.classList.add('hidden');

            if(charts['excel_comparison']) charts['excel_comparison'].destroy();
            const ctx = document.getElementById('chart-excel-comparison').getContext('2d');
            charts['excel_comparison'] = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'Total Pendapatan (Revenue)', data: revenues, backgroundColor: '#4f46e5', borderRadius: 6, maxBarThickness: 32 },
                        { label: 'Total Pengeluaran (Expense)', data: expenses, backgroundColor: '#ef4444', borderRadius: 6, maxBarThickness: 32 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, ticks: { callback: v => 'Rp ' + v.toLocaleString('id-ID') } } }
                }
            });

            const formatIDR = (n) => 'Rp ' + new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 }).format(n || 0);
            const netProfit = totalRevenue - totalExpense;
            const profitMargin = totalRevenue > 0 ? ((netProfit / totalRevenue) * 100).toFixed(1) : 0;
            const statusColor = netProfit >= 0 ? 'text-emerald-600' : 'text-rose-600';
            const statusText = netProfit >= 0 ? 'SURPLUS (Menguntungkan)' : 'DEFISIT (Kerugian)';

            document.getElementById('excel-analysis-text').className = "text-xs text-slate-700 space-y-4 text-left w-full";
            document.getElementById('excel-analysis-text').innerHTML = `
                <div class="grid grid-cols-2 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <div>
                        <p class="text-[10px] uppercase text-slate-400 font-bold">Total Pendapatan</p>
                        <p class="text-sm font-extrabold text-indigo-600">${formatIDR(totalRevenue)}</p>
                    </div>
                    <div>
                        <p class="text-[10px] uppercase text-slate-400 font-bold">Total Pengeluaran</p>
                        <p class="text-sm font-extrabold text-rose-500">${formatIDR(totalExpense)}</p>
                    </div>
                </div>
                <div class="p-4 rounded-xl border ${netProfit >= 0 ? 'bg-emerald-50/50 border-emerald-100' : 'bg-rose-50/50 border-rose-100'}">
                    <p class="text-[10px] uppercase text-slate-400 font-bold">Selisih Bersih (Net Profit)</p>
                    <p class="text-base font-black ${statusColor}">${formatIDR(netProfit)} <span class="text-xs font-bold">(${statusText})</span></p>
                    <p class="text-[11px] font-semibold text-slate-500 mt-1">Rasio profitabilitas bersih berada di kisaran <span class="font-bold text-slate-800">${profitMargin}%</span> dari seluruh omset kas masuk.</p>
                </div>
                <div class="text-[11px] text-slate-500 leading-relaxed bg-indigo-50/20 p-3 rounded-xl border border-indigo-50/30">
                    <i class="fa-solid fa-circle-info text-indigo-500 mr-1"></i> <strong>Rekomendasi Sistem:</strong> 
                    ${netProfit >= 0 
                        ? 'Kondisi finansial dari berkas yang diunggah dinilai aman & sehat. Pertahankan rasio efisiensi pengeluaran anggaran operasional saat ini untuk menjaga tingkat profit margin tetap stabil.' 
                        : 'Peringatan! Tingkat pengeluaran melebihi total pendapatan. Direkomendasikan melakukan audit mendalam pada pos beban variabel atau mengkaji ulang strategi penetapan harga layanan.'
                    }
                </div>
            `;
        }

        function renderActiveView(data) {
            Object.keys(charts).forEach(k => { if(charts[k] && k !== 'excel_comparison') charts[k].destroy(); });
            const formatIDR = (n) => 'Rp ' + new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 }).format(n || 0);

            if (currentView === 'sva') {
                const filterVal = document.getElementById('filter-sva-bulan').value;
                let arr = data['sva'];
                if(filterVal !== 'ALL') arr = arr.filter(d => d.Bulan === filterVal);

                let rev = 0, gross = 0, net = 0;
                arr.forEach(d => {
                    rev += (d.Revenue || 0);
                    if(d.Laba_Kotor === undefined || d.Laba_Kotor === null) d.Laba_Kotor = Math.round(d.Revenue * 0.65);
                    gross += d.Laba_Kotor;
                    net += (d.Net_Income || 0);
                });

                document.getElementById('sva-kpi-1').innerText = formatIDR(rev);
                document.getElementById('sva-kpi-2').innerText = formatIDR(gross);
                document.getElementById('sva-kpi-3').innerText = formatIDR(net);
                document.getElementById('sva-kpi-4').innerText = (rev > 0 ? (net/rev*100).toFixed(1) : 0) + '%';

                const mappedTable = arr.map(d => ({
                    'Bulan': d.Bulan || '-', 'Revenue': d.Revenue, 'Laba_Kotor': d.Laba_Kotor, 'Net_Income': d.Net_Income,
                    'Gross_Profit_Margin': (d.Revenue > 0 ? (d.Laba_Kotor/d.Revenue*100).toFixed(1) : 0) + '%',
                    'Net_Profit_Margin': (d.Revenue > 0 ? (d.Net_Income/d.Revenue*100).toFixed(1) : 0) + '%'
                }));
                buildTable('table-sva', ['Bulan', 'Revenue', 'Laba_Kotor', 'Net_Income', 'Gross_Profit_Margin', 'Net_Profit_Margin'], mappedTable);

                charts['sva_combo'] = new Chart(document.getElementById('chart-sva-finance-line').getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: arr.map(d => d.Bulan),
                        datasets: [
                            { label: 'Revenue', data: arr.map(d => d.Revenue), backgroundColor: '#4f46e5', borderRadius: 6, maxBarThickness: 28 },
                            { label: 'Laba Kotor', data: arr.map(d => d.Laba_Kotor), backgroundColor: '#f59e0b', borderRadius: 6, maxBarThickness: 28 },
                            { label: 'Laba Bersih', data: arr.map(d => d.Net_Income), type: 'line', borderColor: '#10b981', borderWidth: 3.5, pointBackgroundColor: '#10b981', tension: 0.25 }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });

                charts['sva_pie'] = new Chart(document.getElementById('chart-sva-finance-pie').getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: ['Laba Bersih', 'Beban Ops', 'HPP Sistem'],
                        datasets: [{ data: [net, gross - net, rev - gross], backgroundColor: ['#10b981', '#f59e0b', '#ef4444'] }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, cutout: '70%' }
                });
            }
            else if (currentView === 'pm-target') {
                const filterVal = document.getElementById('filter-pm-target-bulan').value;
                let arr = data['pm-target'];
                if(filterVal !== 'ALL') arr = arr.filter(d => d.Bulan === filterVal);

                let t = arr.reduce((acc, c) => acc + (c.Target_WO || 0), 0);
                let r = arr.reduce((acc, c) => acc + (c.Realisasi_WO || 0), 0);
                document.getElementById('pmt-kpi-1').innerText = t + ' WO';
                document.getElementById('pmt-kpi-2').innerText = r + ' WO';
                document.getElementById('pmt-kpi-3').innerText = (t - r) + ' WO';
                document.getElementById('pmt-kpi-4').innerText = Math.round(t > 0 ? (r/t*100) : 0) + '%';

                buildTable('table-pm-target', ['Bulan', 'Target_WO', 'Realisasi_WO'], arr);

                charts['pm_bar'] = new Chart(document.getElementById('chart-pm-target').getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: arr.map(d => d.Bulan),
                        datasets: [
                            { label: 'Target WO', data: arr.map(d => d.Target_WO), backgroundColor: '#cbd5e1', borderRadius: 6 },
                            { label: 'Realisasi WO', data: arr.map(d => d.Realisasi_WO), backgroundColor: '#4f46e5', borderRadius: 6 }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
            else if (currentView === 'pm-curvas') {
                const filterVal = document.getElementById('filter-pm-curvas-minggu').value;
                let arr = data['pm-curvas'];
                if(filterVal !== 'ALL') arr = arr.filter(d => d.Minggu === filterVal);

                charts['pm_curvas'] = new Chart(document.getElementById('chart-pm-curvas').getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: arr.map(d => d.Minggu),
                        datasets: [
                            { label: 'Rencana Kumulatif %', data: arr.map(d => d.Rencana_Kumulatif), borderColor: '#94a3b8', borderDash: [6, 4], tension: 0.1 },
                            { label: 'Aktual Progress %', data: arr.map(d => d.Aktual_Kumulatif), borderColor: '#059669', borderWidth: 4, tension: 0.1 }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
            else if (currentView === 'mbp-rh') {
                const filterVal = document.getElementById('filter-mbp-rh-unit').value;
                let arr = data['mbp-rh'];
                if(filterVal !== 'ALL') arr = arr.filter(d => d.Unit_Genset === filterVal);

                let totalRH = arr.reduce((acc, c) => acc + (c.RH_Akhir || 0), 0);
                let avgDelta = arr.reduce((acc, c) => acc + (c.Delta_RH || 0), 0) / (arr.length || 1);
                let totalTime = arr.reduce((acc, c) => acc + (c.Delta_Time || 0), 0);

                document.getElementById('mbprh-kpi-1').innerText = totalRH.toLocaleString() + ' Jam';
                document.getElementById('mbprh-kpi-2').innerText = avgDelta.toFixed(1) + ' Jam';
                document.getElementById('mbprh-kpi-3').innerText = totalTime.toLocaleString() + ' Jam';

                buildTable('table-mbp-rh', ['Unit_Genset', 'Tanggal', 'RH_Awal', 'RH_Akhir', 'Delta_RH', 'Delta_Time'], arr);

                charts['mbp_rh_bar'] = new Chart(document.getElementById('chart-mbp-rh').getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: arr.map(d => d.Unit_Genset),
                        datasets: [{ label: 'Delta Running Hours', data: arr.map(d => d.Delta_RH), backgroundColor: '#06b6d4', borderRadius: 6 }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
            else if (currentView === 'mbp-bbm') {
                const filterVal = document.getElementById('filter-mbp-bbm-unit').value;
                let arr = data['mbp-bbm'];
                if(filterVal !== 'ALL') arr = arr.filter(d => d.Unit === filterVal);

                let bbm = arr.reduce((acc, c) => acc + (c.Liter_BBM || 0), 0);
                document.getElementById('mbpbbm-kpi-1').innerText = bbm.toLocaleString() + ' Liter';
                document.getElementById('mbpbbm-kpi-2').innerText = (arr.reduce((acc, c) => acc + (c.Rasio_Ltr_Jam || 0), 0) / (arr.length || 1)).toFixed(1) + ' Ltr/Jam';

                buildTable('table-mbp-bbm', ['Tanggal', 'Unit', 'Delta_RH', 'Liter_BBM', 'Rasio_Ltr_Jam'], arr);

                charts['mbp_bbm_bar'] = new Chart(document.getElementById('chart-mbp-bbm').getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: arr.map(d => d.Unit),
                        datasets: [{ label: 'Konsumsi Solar (Liter)', data: arr.map(d => d.Liter_BBM), backgroundColor: '#f59e0b', borderRadius: 6 }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
            else if (currentView.startsWith('asset-')) {
                let arr = data['asset-service'];

                if (currentView === 'asset-service') {
                    const filterVal = document.getElementById('filter-asset-service-lokasi').value;
                    if(filterVal !== 'ALL') arr = arr.filter(d => d.Lokasi === filterVal);
                    buildTable('table-asset-service', ['ID_Asset', 'Nama_Aset', 'Kategori', 'Biaya_Service', 'Lokasi'], arr);
                    charts['asset_svc'] = new Chart(document.getElementById('chart-asset-service').getContext('2d'), { type: 'bar', data: { labels: arr.map(d => d.Nama_Aset), datasets: [{ label: 'Pendanaan Pemeliharaan (IDR)', data: arr.map(d => d.Biaya_Service), backgroundColor: '#ec4899', borderRadius: 6 }] }, options: { responsive: true, maintainAspectRatio: false } });
                }
                else if (currentView === 'asset-depresiasi') {
                    const filterVal = document.getElementById('filter-asset-depresiasi-kat').value;
                    if(filterVal !== 'ALL') arr = arr.filter(d => d.Kategori === filterVal);
                    buildTable('table-asset-depresiasi', ['ID_Asset', 'Nama_Aset', 'Depresiasi'], arr);
                    charts['asset_dep'] = new Chart(document.getElementById('chart-asset-depresiasi').getContext('2d'), { type: 'line', data: { labels: arr.map(d => d.Nama_Aset), datasets: [{ label: 'Penyusutan Buku Berkala', data: arr.map(d => d.Depresiasi), borderColor: '#a855f7', borderWidth: 3 }] }, options: { responsive: true, maintainAspectRatio: false } });
                }
                else if (currentView === 'asset-sewa') {
                    const filterVal = document.getElementById('filter-asset-sewa-lokasi').value;
                    if(filterVal !== 'ALL') arr = arr.filter(d => d.Lokasi === filterVal);
                    buildTable('table-asset-sewa', ['ID_Asset', 'Nama_Aset', 'Biaya_Sewa'], arr);
                    charts['asset_sewa'] = new Chart(document.getElementById('chart-asset-sewa').getContext('2d'), { type: 'bar', data: { labels: arr.map(d => d.Nama_Aset), datasets: [{ label: 'Alokasi Pengeluaran Sewa Unit', data: arr.map(d => d.Biaya_Sewa), backgroundColor: '#3b82f6', borderRadius: 6 }] }, options: { responsive: true, maintainAspectRatio: false } });
                }
            }
        }

        function buildTable(tableId, headers, rowsList) {
            const table = document.getElementById(tableId);
            if (!table) return;
            
            let html = `<thead class="bg-slate-50 text-slate-500 font-bold uppercase border-b border-slate-200/60 tracking-wider"><tr>`;
            headers.forEach(h => { html += `<th class="px-6 py-4">${h.replace(/_/g, ' ')}</th>`; });
            html += `</tr></thead><tbody class="divide-y divide-slate-100 text-slate-700">`;
            
            if(rowsList.length === 0) {
                html += `<tr><td colspan="${headers.length}" class="px-6 py-8 text-center text-slate-400 font-medium">Tidak ada data yang cocok dengan kriteria filter saat ini.</td></tr>`;
            } else {
                rowsList.forEach((row, i) => {
                    html += `<tr class="transition-colors hover:bg-slate-50/80">`;
                    headers.forEach(h => {
                        let val = row[h] !== null && row[h] !== undefined ? row[h] : '-';
                        if (typeof val === 'number' && (h.toLowerCase().includes('revenue') || h.toLowerCase().includes('income') || h.toLowerCase().includes('laba') || h.toLowerCase().includes('biaya') || h.toLowerCase().includes('depresiasi'))) {
                            val = 'Rp ' + new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 }).format(val);
                        }
                        html += `<td class="px-6 py-4 font-semibold text-slate-700">${val}</td>`;
                    });
                    html += `</tr>`;
                });
            }
            html += `</tbody>`;
            table.innerHTML = html;
        }
    </script>
</body>
</html>
   
