import { useState } from 'react'
import { Download, Star, Gamepad2, Image, FileText, Music, Palette, Shield, Rocket, Search, X } from 'lucide-react'
import './App.css'

type Category = 'all' | 'wallpapers' | 'icons' | 'guides' | 'soundtracks' | 'fanart' | 'logos'

interface DownloadItem {
  id: number
  title: string
  description: string
  category: Category
  game: string
  image: string
  fallback: string
  fileSize: string
  downloads: number
  rating: number
}

const games = [
  { name: 'Eve Online', color: 'from-cyan-600 to-blue-800' },
  { name: 'Star Citizen', color: 'from-indigo-600 to-purple-800' },
  { name: 'Elite Dangerous', color: 'from-orange-600 to-red-800' },
  { name: "No Man's Sky", color: 'from-emerald-600 to-teal-800' },
  { name: 'Stellaris', color: 'from-violet-600 to-fuchsia-800' },
  { name: 'X4: Foundations', color: 'from-sky-600 to-cyan-800' },
]

const categories: { key: Category; label: string; icon: typeof Download }[] = [
  { key: 'all', label: 'All', icon: Gamepad2 },
  { key: 'wallpapers', label: 'Wallpapers', icon: Image },
  { key: 'icons', label: 'Icons & Badges', icon: Shield },
  { key: 'guides', label: 'Guides & Manuals', icon: FileText },
  { key: 'soundtracks', label: 'Soundtracks', icon: Music },
  { key: 'fanart', label: 'Fan Art', icon: Palette },
  { key: 'logos', label: 'Logos & Emblems', icon: Star },
]

const downloadItems: DownloadItem[] = [
  // Eve Online
  { id: 1, title: 'Eve Online Nebula Wallpaper Pack', description: 'Stunning 4K wallpapers featuring iconic Eve nebulae, wormholes, and star systems.', category: 'wallpapers', game: 'Eve Online', image: '/images/hero-nebula.jpg', fallback: 'https://placehold.co/600x400/0a1628/38bdf8/png?text=Eve+Nebula+Pack', fileSize: '245 MB', downloads: 18420, rating: 4.9 },
  { id: 2, title: 'Corporation Logo Template Kit', description: 'Create your own Eve Online corporation logos with these layered templates and assets.', category: 'logos', game: 'Eve Online', image: '/images/deep-space.jpg', fallback: 'https://placehold.co/600x400/0a1628/38bdf8/png?text=Corp+Logo+Kit', fileSize: '89 MB', downloads: 7830, rating: 4.7 },
  { id: 3, title: "Fleet Commander's Guide", description: 'Comprehensive PDF guide to fleet commanding in Eve Online — from small gang to large fleet warfare.', category: 'guides', game: 'Eve Online', image: '/images/cosmos.jpg', fallback: 'https://placehold.co/600x400/0a1628/38bdf8/png?text=FC+Guide', fileSize: '32 MB', downloads: 24510, rating: 4.8 },
  { id: 4, title: 'Ship Blueprint Icon Pack', description: '500+ high-resolution icons of every ship class in Eve Online — from frigates to titans.', category: 'icons', game: 'Eve Online', image: '/images/spaceship.jpg', fallback: 'https://placehold.co/600x400/0a1628/38bdf8/png?text=Ship+Icons', fileSize: '156 MB', downloads: 12100, rating: 4.6 },
  { id: 5, title: 'New Eden Ambient Soundtrack', description: 'Hours of ambient space music inspired by the Eve Online universe — perfect for gaming sessions.', category: 'soundtracks', game: 'Eve Online', image: '/images/stars.jpg', fallback: 'https://placehold.co/600x400/0a1628/38bdf8/png?text=Eve+Soundtrack', fileSize: '380 MB', downloads: 9640, rating: 4.9 },
  { id: 6, title: 'Capsuleer Fan Art Collection', description: 'Community-curated fan art featuring capsuleers, ships, and epic battle scenes from New Eden.', category: 'fanart', game: 'Eve Online', image: '/images/galaxy.jpg', fallback: 'https://placehold.co/600x400/0a1628/38bdf8/png?text=Eve+Fan+Art', fileSize: '410 MB', downloads: 6250, rating: 4.5 },
  // Star Citizen
  { id: 7, title: 'Star Citizen Ship Wallpapers', description: "High-res wallpapers featuring Star Citizen's most iconic ships in stunning detail.", category: 'wallpapers', game: 'Star Citizen', image: '/images/spaceship.jpg', fallback: 'https://placehold.co/600x400/1e1b4b/818cf8/png?text=SC+Ships', fileSize: '310 MB', downloads: 15200, rating: 4.8 },
  { id: 8, title: 'Organization Emblem Creator', description: 'Design stunning org emblems with this template pack for Star Citizen organizations.', category: 'logos', game: 'Star Citizen', image: '/images/planet.jpg', fallback: 'https://placehold.co/600x400/1e1b4b/818cf8/png?text=Org+Emblems', fileSize: '67 MB', downloads: 5400, rating: 4.4 },
  { id: 9, title: "Pilot's Trading Guide", description: 'Master the art of trading across the verse with routes, tips, and profit calculators.', category: 'guides', game: 'Star Citizen', image: '/images/cosmos.jpg', fallback: 'https://placehold.co/600x400/1e1b4b/818cf8/png?text=Trading+Guide', fileSize: '28 MB', downloads: 11800, rating: 4.6 },
  { id: 10, title: 'Verse Ambient Mix', description: 'Atmospheric soundscapes from across the Star Citizen universe — quantum travel vibes.', category: 'soundtracks', game: 'Star Citizen', image: '/images/deep-space.jpg', fallback: 'https://placehold.co/600x400/1e1b4b/818cf8/png?text=SC+Ambient', fileSize: '290 MB', downloads: 7100, rating: 4.7 },
  // Elite Dangerous
  { id: 11, title: 'Elite Dangerous Galaxy Wallpapers', description: 'Breathtaking views from across the Milky Way — planetary landings, stellar phenomena, and more.', category: 'wallpapers', game: 'Elite Dangerous', image: '/images/galaxy.jpg', fallback: 'https://placehold.co/600x400/431407/fb923c/png?text=ED+Galaxy', fileSize: '280 MB', downloads: 13400, rating: 4.7 },
  { id: 12, title: "Commander's Exploration Handbook", description: 'The definitive guide to deep-space exploration in Elite Dangerous — neutron highways, fuel scooping, and more.', category: 'guides', game: 'Elite Dangerous', image: '/images/stars.jpg', fallback: 'https://placehold.co/600x400/431407/fb923c/png?text=Exploration+Guide', fileSize: '45 MB', downloads: 19200, rating: 4.9 },
  { id: 13, title: 'Squadron Badge Pack', description: '200+ squadron badges and rank insignias for Elite Dangerous commanders.', category: 'icons', game: 'Elite Dangerous', image: '/images/space-battle.jpg', fallback: 'https://placehold.co/600x400/431407/fb923c/png?text=Squad+Badges', fileSize: '78 MB', downloads: 4600, rating: 4.3 },
  { id: 14, title: 'Thargoid Encounter Fan Art', description: 'Dramatic fan art depicting Thargoid encounters — interceptors, scouts, and epic battles.', category: 'fanart', game: 'Elite Dangerous', image: '/images/deep-space.jpg', fallback: 'https://placehold.co/600x400/431407/fb923c/png?text=Thargoid+Art', fileSize: '350 MB', downloads: 8700, rating: 4.6 },
  // No Man's Sky
  { id: 15, title: 'Procedural Worlds Wallpaper Pack', description: "Alien landscapes, vibrant planets, and exotic creatures from across the No Man's Sky universe.", category: 'wallpapers', game: "No Man's Sky", image: '/images/planet.jpg', fallback: 'https://placehold.co/600x400/064e3b/34d399/png?text=NMS+Worlds', fileSize: '195 MB', downloads: 11000, rating: 4.5 },
  { id: 16, title: 'Base Building Blueprints', description: 'Detailed building guides with layouts for optimal bases — from starter shelters to mega complexes.', category: 'guides', game: "No Man's Sky", image: '/images/cosmos.jpg', fallback: 'https://placehold.co/600x400/064e3b/34d399/png?text=Base+Blueprints', fileSize: '52 MB', downloads: 16300, rating: 4.8 },
  { id: 17, title: "Traveller's Soundtrack Remix", description: "Fan-made remixes of the iconic No Man's Sky soundtrack — chill exploration vibes.", category: 'soundtracks', game: "No Man's Sky", image: '/images/stars.jpg', fallback: 'https://placehold.co/600x400/064e3b/34d399/png?text=NMS+Remixes', fileSize: '220 MB', downloads: 5800, rating: 4.4 },
  // Stellaris
  { id: 18, title: 'Stellaris Empire Wallpapers', description: 'Grand strategy meets cosmic beauty — empire maps, fleet formations, and galactic vistas.', category: 'wallpapers', game: 'Stellaris', image: '/images/hero-nebula.jpg', fallback: 'https://placehold.co/600x400/4a044e/d946ef/png?text=Stellaris+Empire', fileSize: '175 MB', downloads: 8900, rating: 4.6 },
  { id: 19, title: 'Species Portrait Pack', description: 'Fan-made species portraits compatible with Stellaris — over 100 unique alien designs.', category: 'fanart', game: 'Stellaris', image: '/images/galaxy.jpg', fallback: 'https://placehold.co/600x400/4a044e/d946ef/png?text=Species+Portraits', fileSize: '134 MB', downloads: 7200, rating: 4.5 },
  { id: 20, title: 'Galactic Domination Guide', description: 'Min-max your way to galactic supremacy — build orders, tech paths, and fleet compositions.', category: 'guides', game: 'Stellaris', image: '/images/space-battle.jpg', fallback: 'https://placehold.co/600x400/4a044e/d946ef/png?text=Strategy+Guide', fileSize: '38 MB', downloads: 21000, rating: 4.9 },
  // X4: Foundations
  { id: 21, title: 'X4 Station Wallpapers', description: 'Massive space stations, trade routes, and fleet battles from the X4 universe.', category: 'wallpapers', game: 'X4: Foundations', image: '/images/spaceship.jpg', fallback: 'https://placehold.co/600x400/0c4a6e/38bdf8/png?text=X4+Stations', fileSize: '160 MB', downloads: 4200, rating: 4.3 },
  { id: 22, title: "Empire Builder's Manual", description: 'From small trader to sector overlord — the complete guide to building your X4 empire.', category: 'guides', game: 'X4: Foundations', image: '/images/cosmos.jpg', fallback: 'https://placehold.co/600x400/0c4a6e/38bdf8/png?text=Empire+Manual', fileSize: '41 MB', downloads: 6100, rating: 4.7 },
  { id: 23, title: 'Faction Logo Collection', description: 'Every faction logo from X4: Foundations in SVG and PNG format — perfect for modding.', category: 'logos', game: 'X4: Foundations', image: '/images/deep-space.jpg', fallback: 'https://placehold.co/600x400/0c4a6e/38bdf8/png?text=Faction+Logos', fileSize: '23 MB', downloads: 3400, rating: 4.2 },
  { id: 24, title: 'X4 Ambient Space Audio', description: 'Immersive ambient audio loops from the X4 universe — engine hums, station ambience, and more.', category: 'soundtracks', game: 'X4: Foundations', image: '/images/stars.jpg', fallback: 'https://placehold.co/600x400/0c4a6e/38bdf8/png?text=X4+Audio', fileSize: '180 MB', downloads: 2900, rating: 4.4 },
]

function App() {
  const [selectedGame, setSelectedGame] = useState<string>('all')
  const [selectedCategory, setSelectedCategory] = useState<Category>('all')
  const [searchQuery, setSearchQuery] = useState('')

  const filteredItems = downloadItems.filter(item => {
    const matchesGame = selectedGame === 'all' || item.game === selectedGame
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory
    const matchesSearch = searchQuery === '' ||
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.game.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesGame && matchesCategory && matchesSearch
  })

  const totalDownloads = downloadItems.reduce((sum, item) => sum + item.downloads, 0)

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>, fallback: string) => {
    const target = e.target as HTMLImageElement
    target.src = fallback
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="/images/hero-nebula.jpg"
            alt="Space nebula background"
            className="w-full h-full object-cover opacity-30"
            onError={(e) => handleImageError(e, 'https://placehold.co/1920x600/0a0a1a/38bdf8/png?text=Space+Downloads')}
          />
          <div className="absolute inset-0 bg-gradient-to-b from-gray-950/60 via-gray-950/40 to-gray-950" />
        </div>
        <div className="relative max-w-7xl mx-auto px-4 py-20 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <Rocket className="w-10 h-10 text-cyan-400" />
              <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                Space Games Downloads
              </h1>
            </div>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto mt-4">
              Wallpapers, guides, soundtracks, fan art, and more for your favorite space games.
              Free community-curated paraphernalia.
            </p>
            <div className="flex items-center justify-center gap-8 mt-8 text-sm text-gray-400">
              <div className="flex items-center gap-2">
                <Download className="w-4 h-4 text-cyan-400" />
                <span>{totalDownloads.toLocaleString()} total downloads</span>
              </div>
              <div className="flex items-center gap-2">
                <Gamepad2 className="w-4 h-4 text-purple-400" />
                <span>{games.length} games</span>
              </div>
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 text-yellow-400" />
                <span>{downloadItems.length} items</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Game Selector */}
        <div className="mb-8">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Filter by Game</h2>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => setSelectedGame('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                selectedGame === 'all'
                  ? 'bg-cyan-600 text-white shadow-lg shadow-cyan-600/25'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              All Games
            </button>
            {games.map(game => (
              <button
                key={game.name}
                onClick={() => setSelectedGame(game.name)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  selectedGame === game.name
                    ? `bg-gradient-to-r ${game.color} text-white shadow-lg`
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                {game.name}
              </button>
            ))}
          </div>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search downloads..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-10 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap gap-2 mb-8 border-b border-gray-800 pb-4">
          {categories.map(cat => {
            const Icon = cat.icon
            return (
              <button
                key={cat.key}
                onClick={() => setSelectedCategory(cat.key)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  selectedCategory === cat.key
                    ? 'bg-gray-800 text-cyan-400 ring-1 ring-cyan-400/30'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
                }`}
              >
                <Icon className="w-4 h-4" />
                {cat.label}
              </button>
            )
          })}
        </div>

        {/* Results Count */}
        <div className="mb-6 text-sm text-gray-400">
          Showing {filteredItems.length} of {downloadItems.length} items
          {selectedGame !== 'all' && <span className="text-cyan-400"> for {selectedGame}</span>}
          {selectedCategory !== 'all' && <span className="text-purple-400"> in {categories.find(c => c.key === selectedCategory)?.label}</span>}
        </div>

        {/* Download Cards Grid */}
        {filteredItems.length === 0 ? (
          <div className="text-center py-20">
            <Gamepad2 className="w-16 h-16 text-gray-700 mx-auto mb-4" />
            <p className="text-xl text-gray-500">No downloads found</p>
            <p className="text-gray-600 mt-2">Try adjusting your filters or search terms</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredItems.map(item => {
              const gameInfo = games.find(g => g.name === item.game)
              return (
                <div
                  key={item.id}
                  className="group bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-gray-600 transition-all duration-300 hover:shadow-xl hover:shadow-cyan-900/10"
                >
                  {/* Card Image */}
                  <div className="relative h-48 overflow-hidden">
                    <img
                      src={item.image}
                      alt={item.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      onError={(e) => handleImageError(e, item.fallback)}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/20 to-transparent" />
                    <div className="absolute top-3 left-3">
                      <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r ${gameInfo?.color || 'from-gray-600 to-gray-800'} text-white shadow-lg`}>
                        {item.game}
                      </span>
                    </div>
                    <div className="absolute top-3 right-3">
                      <span className="inline-block px-2 py-1 rounded-md text-xs font-medium bg-black/60 text-gray-300 backdrop-blur-sm">
                        {item.fileSize}
                      </span>
                    </div>
                  </div>

                  {/* Card Content */}
                  <div className="p-5">
                    <h3 className="text-lg font-bold text-white mb-2 group-hover:text-cyan-400 transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-sm text-gray-400 mb-4 line-clamp-2">
                      {item.description}
                    </p>

                    {/* Stats Row */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-1">
                        {Array.from({ length: 5 }, (_, i) => (
                          <Star
                            key={i}
                            className={`w-3.5 h-3.5 ${
                              i < Math.floor(item.rating) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-600'
                            }`}
                          />
                        ))}
                        <span className="text-xs text-gray-500 ml-1">{item.rating}</span>
                      </div>
                      <div className="flex items-center gap-1 text-xs text-gray-500">
                        <Download className="w-3.5 h-3.5" />
                        {item.downloads.toLocaleString()}
                      </div>
                    </div>

                    {/* Download Button */}
                    <button className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-lg font-medium text-sm transition-all duration-200 shadow-lg shadow-cyan-600/20 hover:shadow-cyan-500/30">
                      <Download className="w-4 h-4" />
                      Download
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        )}

        {/* Footer */}
        <footer className="mt-20 pt-8 border-t border-gray-800 text-center text-gray-500 text-sm">
          <p>Community-curated space game paraphernalia. All fan content is shared under fair use.</p>
          <p className="mt-2">Not affiliated with CCP Games, Cloud Imperium Games, Frontier Developments, Hello Games, Paradox Interactive, or Egosoft.</p>
        </footer>
      </div>
    </div>
  )
}

export default App
