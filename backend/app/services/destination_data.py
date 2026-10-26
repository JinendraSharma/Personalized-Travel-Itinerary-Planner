"""Destination knowledge database and intelligent itinerary generation engine.

Provides authentic, rich, and culturally accurate landmark, culinary,
and transit data for major global & Indian destinations, plus a universal
procedural generator for any destination worldwide.
"""

from typing import Dict, Any, List, Optional
import hashlib
import re

# Comprehensive curated database of destinations with authentic local sights, foods, and transport
DESTINATION_DATABASE: Dict[str, Dict[str, Any]] = {
    "indore": {
        "city": "Indore",
        "state_country": "Madhya Pradesh, India",
        "tagline": "Cleanest City of India & Central India's Foodie Capital",
        "transit_types": ["E-Rickshaw", "Auto-rickshaw", "iBus (BRTS)", "App-Cab"],
        "local_specialties": ["Poha Jalebi with Ratlami Sev", "Bhutte Ka Kees", "Garadu", "Joshi Dahi Vada", "Khopra Patties", "Dal Bafla", "Malpua", "Shikanji (Indori style)"],
        "days": [
            {
                "theme": "Royal Holkar Heritage & The Legendary Sarafa Night Food Trail",
                "summary": "Immerse in the historic heart of Indore, exploring 18th-century Holkar dynasty palaces and capping off with Asia's most famous midnight street food bazaar.",
                "morning": {
                    "title": "Holkar Grandeur at Rajwada Palace & Poha-Jalebi Breakfast",
                    "description": "Start with authentic Indori Poha topped with crispy Ratlami Sev and piping hot Jalebis at Prashant / Apna Sweets. Then marvel at the majestic 7-story Rajwada Palace, a blend of Maratha, Mughal, and French architecture.",
                    "location": "Rajwada, MG Road",
                    "category": "Heritage & Architecture",
                    "neighborhood": "Old Indore Heritage Quarter",
                    "transit_time": "5 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.25,
                },
                "afternoon": {
                    "title": "Versailles-inspired Splendor at Lal Bagh Palace & Marothiya Bazaar",
                    "description": "Tour the lavish Lal Bagh Palace set on the banks of Khan River, featuring Italian marble, Belgian stained glass, and Buckingham Palace replica gates. Stroll through vibrant Marothiya Bazaar for traditional Maheshwari and Chanderi sarees.",
                    "location": "Lal Bagh Palace, Nai Duniya",
                    "category": "Culture & Shopping",
                    "neighborhood": "Lal Bagh Precinct",
                    "transit_time": "12 mins via Auto-rickshaw",
                    "transit_mode": "Auto-rickshaw",
                    "cost_pct": 0.35,
                },
                "evening": {
                    "title": "Asia's Famous Sarafa Night Food Safari (Garadu, Bhutte Ka Kees & Flying Dahi Vada)",
                    "description": "As jewelry shops close at 8 PM, the street transforms into a sensory food haven. Indulge in winter-spiced Garadu, creamy grated corn Bhutte Ka Kees, coconut-stuffed Khopra Patties at Vijay Chaat, and Joshi Ji's acrobatic Dahi Vada.",
                    "location": "Sarafa Bazaar, Old City",
                    "category": "Night Food Safari",
                    "neighborhood": "Sarafa Night Food Enclave",
                    "transit_time": "8 mins via E-Rickshaw",
                    "transit_mode": "E-Rickshaw",
                    "cost_pct": 0.40,
                },
            },
            {
                "theme": "Architectural Gems, Spiritual Serenity & 56-Dukan Gastronomy",
                "summary": "Discover the intricate glass mosaics of Kanch Mandir, the ancient devotion at Khajrana Ganesh, and the world-renowned Chappan Dukan food street.",
                "morning": {
                    "title": "Glistening Glass Marvel at Kanch Mandir & Historic Itwaria Bazaar",
                    "description": "Visit the 120-year-old Jain Glass Temple (Kanch Mandir), adorned entirely with Chinese glass tiles, Belgian cut-glass mirrors, and crystal chandeliers depicting Jain scriptures. Walk through the fragrant spice lanes of Itwaria Bazaar.",
                    "location": "Itwaria Bazaar, Malharganj",
                    "category": "Spiritual & Art",
                    "neighborhood": "Malharganj Historic Ward",
                    "transit_time": "8 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.20,
                },
                "afternoon": {
                    "title": "Feast at Chappan Dukan (56 Shops) & Authentic Malwi Dal Bafla Lunch",
                    "description": "Head to Indore's cleanest food street '56 Dukan'. Savor crispy hotdogs at Johnny Hot Dog (pioneering Indian burger), Shreemaya pastries, and a regal lunch of Dal Bafla with fragrant ghee and churma ladoos.",
                    "location": "Chappan Dukan, New Palasia",
                    "category": "Gastronomy & Culture",
                    "neighborhood": "Palasia Food Corridor",
                    "transit_time": "14 mins via iBus (BRTS)",
                    "transit_mode": "iBus BRTS",
                    "cost_pct": 0.45,
                },
                "evening": {
                    "title": "Devotion at Khajrana Ganesh Temple & Sunset at Pipliyapala Regional Park",
                    "description": "Seek blessings at the historic Khajrana Ganesh Temple, originally established by Queen Ahilyabai Holkar in 1735. Conclude your evening watching musical fountain shows along the serene Pipliyapala lakefront promenade.",
                    "location": "Khajrana & Pipliyapala Lake",
                    "category": "Leisure & Spiritual",
                    "neighborhood": "East Indore Enclave",
                    "transit_time": "15 mins via Auto-rickshaw",
                    "transit_mode": "Auto-rickshaw",
                    "cost_pct": 0.35,
                },
            },
            {
                "theme": "Nature Escapes, Waterfalls & Malwi Countryside Charm",
                "summary": "Venture into the lush Vindhya valleys surrounding Indore to witness scenic waterfalls, colonial hill-cantonment history, and tranquil lake vistas.",
                "morning": {
                    "title": "Scenic Excursion to Patalpani Waterfall & Mhow Cantt Heritage",
                    "description": "Take a scenic drive through the Vindhya hills to the roaring 300-ft Patalpani Waterfall. Stop by historic Mhow (Dr. Ambedkar Nagar) with its colonial railway bridges, military cantonment greenery, and roadside roasted corn stalls.",
                    "location": "Patalpani, Mhow Valley",
                    "category": "Nature & Scenic Trails",
                    "neighborhood": "Vindhyachal Foothills",
                    "transit_time": "40 mins scenic drive",
                    "transit_mode": "Private Cab",
                    "cost_pct": 0.35,
                },
                "afternoon": {
                    "title": "Lakeside Relaxation & Water Sports at Choral Dam",
                    "description": "Unwind by the tranquil turquoise waters of Choral Dam. Enjoy pedal-boating, peaceful waterfront photography, and fresh riverside snacks amidst verdant hillocks and cool Malwa breezes.",
                    "location": "Choral Dam, Khandwa Road",
                    "category": "Lakes & Adventure",
                    "neighborhood": "Choral Valley Retreat",
                    "transit_time": "20 mins via Cab",
                    "transit_mode": "Cab",
                    "cost_pct": 0.35,
                },
                "evening": {
                    "title": "Sunset at Ralamandal Wildlife Sanctuary & Malwi Cultural Village Dinner",
                    "description": "Climb up to the historic Holkar hunting lodge (Shikargah) at Ralamandal Wildlife Sanctuary for a sunset panorama over Indore. Finish the day with live folk performances and clay-oven roasted delicacies at Nakhrali Dhani village resort.",
                    "location": "Ralamandal & Rau-Pithampur Corridor",
                    "category": "Wildlife & Folk Culture",
                    "neighborhood": "Bypass Green Belt",
                    "transit_time": "25 mins via Cab",
                    "transit_mode": "Cab",
                    "cost_pct": 0.30,
                },
            },
        ],
    },
    "jaipur": {
        "city": "Jaipur",
        "state_country": "Rajasthan, India",
        "tagline": "The Pink City & Regal Citadel of the Kachwaha Rajputs",
        "transit_types": ["Pink City E-Rickshaw", "Jaipur Metro", "Auto-rickshaw", "Heritage Cab"],
        "local_specialties": ["Dal Baati Churma", "Pyaaz Kachori at Rawat", "Ghewar at LMB", "Laal Maas", "Mawa Kachori", "Lassi at Lassiwala MI Road", "Ker Sangri"],
        "days": [
            {
                "theme": "The Royal Walled City: Palaces of Wind, Astronomy & Maharajas",
                "summary": "Step into the terracotta-pink walled city of Jaipur, discovering fairy-tale latticework, world-heritage astronomical instruments, and royal residences.",
                "morning": {
                    "title": "Sunrise Splendor at Hawa Mahal & Pink City Heritage Walk",
                    "description": "Catch early golden rays illuminating the 953 honeycomb sandstone casements of Hawa Mahal (Palace of Winds). Stroll through the heritage arcades of Badi Choupad and enjoy Kulhad Chai with piping hot Pyaaz Kachoris.",
                    "location": "Hawa Mahal, Badi Choupad",
                    "category": "Heritage & Architecture",
                    "neighborhood": "Old Walled Pink City",
                    "transit_time": "Walk & E-Rickshaw",
                    "transit_mode": "E-Rickshaw",
                    "cost_pct": 0.30,
                },
                "afternoon": {
                    "title": "City Palace Peacock Courtyard & Jantar Mantar Observatory",
                    "description": "Explore the majestic City Palace, featuring Mubarak Mahal royal armory and the stunning Peacock Gate at Pritam Niwas Chowk. Next door, wander through UNESCO Jantar Mantar to see the world's largest stone sundial (Samrat Yantra).",
                    "location": "Jaleb Chowk, Old City",
                    "category": "Palaces & Astronomy",
                    "neighborhood": "Royal Palace Enclave",
                    "transit_time": "4 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.40,
                },
                "evening": {
                    "title": "Sunset Over Pink City from Nahargarh Fort & Dinner at Padao",
                    "description": "Ascend the Aravalli hills to Nahargarh Fort ('Abode of Tigers'). Marvel at the 360-degree twilight view as Jaipur's lights twinkle below, and relish dinner with Rajput cocktails at the cliffside Padao restaurant.",
                    "location": "Nahargarh Fort, Aravalli Hills",
                    "category": "Fortresses & Sunset Vistas",
                    "neighborhood": "Aravalli Ridge",
                    "transit_time": "25 mins scenic winding drive",
                    "transit_mode": "Cab",
                    "cost_pct": 0.30,
                },
            },
            {
                "theme": "Legendary Amber Fort, Mirror Palaces & Royal Craft Bazaars",
                "summary": "Ascend the grand ramparts of Amber Fort, uncover hidden geometric stepwells, and shop for heirloom gemstones and block-printed textiles.",
                "morning": {
                    "title": "Amber Fort Ramparts & The Dazzling Sheesh Mahal (Mirror Palace)",
                    "description": "Journey to historic Amer to explore the grand courtyards, Diwan-e-Aam, and the breathtaking Sheesh Mahal where a single candle illuminates the entire hall. Catch mirror reflections of the fort in Maota Lake.",
                    "location": "Amer Fort, Devisinghpura",
                    "category": "UNESCO Fortress",
                    "neighborhood": "Amer Heritage Corridor",
                    "transit_time": "20 mins via AC Express Bus / Cab",
                    "transit_mode": "Cab",
                    "cost_pct": 0.40,
                },
                "afternoon": {
                    "title": "Panna Meena Ka Kund Stepwell & Jal Mahal Water Palace Promenade",
                    "description": "Photograph the mesmerizing symmetrical staircases of Panna Meena Ka Kund ancient stepwell. On the return route, pause by the edge of Man Sagar Lake to admire the floating palace of Jal Mahal surrounded by birds and water reflections.",
                    "location": "Amer Stepwell & Jal Mahal, Amer Road",
                    "category": "Architecture & Photography",
                    "neighborhood": "Man Sagar Lake Enclave",
                    "transit_time": "10 mins via Auto-rickshaw",
                    "transit_mode": "Auto-rickshaw",
                    "cost_pct": 0.25,
                },
                "evening": {
                    "title": "Johari Bazaar Gemstone Alley & Traditional Feast at Laxmi Mishtan Bhandar (LMB)",
                    "description": "Dabble in sparkling Kundan-Meenakari jewelry at Johari Bazaar and bright Bandhani dupattas at Bapu Bazaar. Cap the evening with a royal Rajasthani Thali and authentic Paneer Ghewar at the century-old LMB restaurant.",
                    "location": "Johari Bazaar & LMB, Pink City",
                    "category": "Bazaars & Fine Dining",
                    "neighborhood": "Johari Bazaar District",
                    "transit_time": "12 mins via E-Rickshaw",
                    "transit_mode": "E-Rickshaw",
                    "cost_pct": 0.35,
                },
            },
            {
                "theme": "Regal Arts, Cannon Forts & Vibrant Rajasthani Folklore",
                "summary": "Inspect the colossal Jaivana cannon at Jaigarh Fort, marvel at Albert Hall museum treasures, and experience vibrant folk arts at Chokhi Dhani.",
                "morning": {
                    "title": "Jaigarh Fort & The World's Largest Wheeled Cannon (Jaivana)",
                    "description": "Climb up to military bastion Jaigarh Fort overlooking Amber. Walk through the underground escape passages, weapon foundry, and inspect Jaivana, once the world's most formidable wheeled cannon.",
                    "location": "Jaigarh Fort, Cheel ka Teela",
                    "category": "Military Forts & Vistas",
                    "neighborhood": "Amer Hilltop",
                    "transit_time": "10 mins uphill cab",
                    "transit_mode": "Cab",
                    "cost_pct": 0.30,
                },
                "afternoon": {
                    "title": "Albert Hall Museum Treasures & Creamy Lassi at Lassiwala MI Road",
                    "description": "Marvel at the Indo-Saracenic Albert Hall Museum surrounded by hundreds of fluttering pigeons in Ram Niwas Garden. Walk over to iconic Lassiwala on MI Road (operating since 1944) for thick malai lassi served in earthen kulhads.",
                    "location": "Ram Niwas Garden & MI Road",
                    "category": "Museums & Gastronomy",
                    "neighborhood": "MI Road & C-Scheme",
                    "transit_time": "18 mins via Jaipur Metro / Cab",
                    "transit_mode": "Jaipur Metro",
                    "cost_pct": 0.30,
                },
                "evening": {
                    "title": "Rajasthani Folk Dances, Fire Eaters & Dal Baati at Chokhi Dhani Resort",
                    "description": "Immerse in an authentic ethnic village carnival featuring Kalbelia dancers, puppet shows, camel rides, and an extravagant traditional Rajasthani dinner served on leaf platters with unlimited Ghee and Churma.",
                    "location": "Chokhi Dhani, Tonk Road",
                    "category": "Folk Culture & Feast",
                    "neighborhood": "South Jaipur Cultural Enclave",
                    "transit_time": "30 mins via Cab",
                    "transit_mode": "Cab",
                    "cost_pct": 0.40,
                },
            },
        ],
    },
    "delhi": {
        "city": "Delhi",
        "state_country": "India",
        "tagline": "The City of Djinns: 8 Historic Cities in One Vibrant Capital",
        "transit_types": ["Delhi Metro (World-Class)", "E-Rickshaw", "App-Cab", "DTC Electric Bus"],
        "local_specialties": ["Chole Bhature at Sita Ram Diwan Chand", "Paranthe Wali Gali", "Old Delhi Butter Chicken", "Karim's Mutton Seekh", "Daulat Ki Chaat", "Momos at Majnu Ka Tila"],
        "days": [
            {
                "theme": "Shahjahanabad: Mughal Forts, Spice Bazaars & Royal Cuisine",
                "summary": "Walk the bustling alleys of Old Delhi, explore Mughal architecture, and taste recipes preserved for centuries.",
                "morning": {
                    "title": "Red Fort (Lal Qila) & The Grand Jama Masjid",
                    "description": "Explore the sandstone citadel of Emperor Shah Jahan and ascend the southern minaret of Jama Masjid for sprawling vistas over Old Delhi. Enjoy warm Bedmi Puri with spicy aloo at Ram Swaroop.",
                    "location": "Chandni Chowk, Old Delhi",
                    "category": "Heritage & Monuments",
                    "neighborhood": "Shahjahanabad Walled City",
                    "transit_time": "Yellow Line Metro to Chandni Chowk",
                    "transit_mode": "Delhi Metro",
                    "cost_pct": 0.30,
                },
                "afternoon": {
                    "title": "Asia's Largest Spice Market (Khari Baoli) & Paranthe Wali Gali",
                    "description": "Ride a cycle-rickshaw through the pungent, colorful sack-filled alleys of Khari Baoli spice bazaar. Stop at Paranthe Wali Gali for deep-fried stuffed parathas filled with paneer, rabri, or spiced potatoes.",
                    "location": "Khari Baoli & Dariba Kalan",
                    "category": "Bazaars & Street Food",
                    "neighborhood": "Old Delhi Core",
                    "transit_time": "Cycle Rickshaw (10 mins)",
                    "transit_mode": "Cycle Rickshaw",
                    "cost_pct": 0.35,
                },
                "evening": {
                    "title": "India Gate Stroll along Kartavya Path & Pandara Road Dining",
                    "description": "Witness the Amar Jawan Jyoti at India Gate illuminated against the twilight sky. Head to Pandara Road Market for legendary Mughlai butter chicken and dal makhani at Gulati.",
                    "location": "Kartavya Path & Pandara Road",
                    "category": "Monuments & Dining",
                    "neighborhood": "Central Lutyens' Delhi",
                    "transit_time": "15 mins via Metro / Cab",
                    "transit_mode": "Delhi Metro",
                    "cost_pct": 0.35,
                },
            },
            {
                "theme": "Sultanate Marvels, Urban Art & Green Sanctuaries",
                "summary": "Journey through South Delhi's towering UNESCO minarets, vibrant street art murals, and historic garden tombs.",
                "morning": {
                    "title": "UNESCO Qutub Minar & The Ancient Rust-Free Iron Pillar",
                    "description": "Inspect the intricate fluted sandstone minaret rising 73 meters and the mysterious 1,600-year-old Gupta-era iron pillar that has never rusted.",
                    "location": "Mehrauli Archaeological Complex",
                    "category": "UNESCO World Heritage",
                    "neighborhood": "Mehrauli Heritage Zone",
                    "transit_time": "Yellow Line to Qutab Minar",
                    "transit_mode": "Delhi Metro",
                    "cost_pct": 0.35,
                },
                "afternoon": {
                    "title": "Humayun's Tomb (Precursor to the Taj Mahal) & Lodhi Art District",
                    "description": "Admire the symmetrical Charbagh gardens and Persian dome of Humayun's Tomb. Walk through Lodhi Colony to view towering public street murals created by global artists.",
                    "location": "Nizamuddin East & Lodhi Colony",
                    "category": "Art & Architecture",
                    "neighborhood": "Lodhi Estate",
                    "transit_time": "12 mins via Auto-rickshaw",
                    "transit_mode": "Auto-rickshaw",
                    "cost_pct": 0.35,
                },
                "evening": {
                    "title": "Sunset by Hauz Khas Fort Lake & Bohemian Cafes",
                    "description": "Watch ducks and egrets at the 13th-century water reservoir from Hauz Khas medieval madrasa ruins. Transition into the village's chic rooftop bistros for craft cocktails and indie music.",
                    "location": "Hauz Khas Village",
                    "category": "Nightlife & Heritage",
                    "neighborhood": "Hauz Khas Enclave",
                    "transit_time": "15 mins via Cab",
                    "transit_mode": "Cab",
                    "cost_pct": 0.30,
                },
            },
        ],
    },
    "mumbai": {
        "city": "Mumbai",
        "state_country": "Maharashtra, India",
        "tagline": "The City of Dreams & Coastal Financial Metropolis",
        "transit_types": ["Mumbai Local Train", "Mumbai Metro", "Black & Yellow (Kaali Peeli) Taxi", "Harbor Ferry"],
        "local_specialties": ["Vada Pav", "Pav Bhaji at Sardar/Cannon", "Bombay Duck Fry", "Bhel Puri at Chowpatty", "Irani Chai & Bun Maska at Britannia & Co."],
        "days": [
            {
                "theme": "Colonial South Bombay, Harbor Gateways & The Queen's Necklace",
                "summary": "Explore grand Gothic-Victorian architecture, seaside promenades, and old-world Irani cafe culture.",
                "morning": {
                    "title": "Gateway of India & Gothic Splendor of Chhatrapati Shivaji Terminus (CST)",
                    "description": "Start at the iconic basalt arch of Gateway of India overlooking Mumbai Harbor and the historic Taj Mahal Palace Hotel. Take a taxi past the UNESCO Victorian Gothic train terminus at CST.",
                    "location": "Apollo Bunder & Fort, South Mumbai",
                    "category": "Historic Landmarks",
                    "neighborhood": "Colaba & Fort District",
                    "transit_time": "Kaali Peeli Taxi (10 mins)",
                    "transit_mode": "Taxi",
                    "cost_pct": 0.30,
                },
                "afternoon": {
                    "title": "Kala Ghoda Art Precinct & Berry Pulao at Britannia & Co.",
                    "description": "Browse art galleries, indie boutiques, and colonial archways in Kala Ghoda. Savor legendary Parsi Berry Pulao, Sali Boti, and caramel custard at heritage Irani cafe Britannia & Co.",
                    "location": "Kala Ghoda & Ballard Estate",
                    "category": "Arts, Heritage & Dining",
                    "neighborhood": "Kala Ghoda Heritage Mile",
                    "transit_time": "5 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.40,
                },
                "evening": {
                    "title": "Sunset Breeze along Marine Drive (Queen's Necklace) & Girgaon Chowpatty Chaat",
                    "description": "Sit on the promenade tetra-pods as the sun sets over the Arabian Sea and the arc of city lights flickers on like a string of pearls. Munch on spicy Sev Puri and Bhel Puri at Girgaon Chowpatty.",
                    "location": "Marine Drive & Girgaon Chowpatty",
                    "category": "Promenade & Beach Chaat",
                    "neighborhood": "Marine Lines Coastal Arc",
                    "transit_time": "8 mins taxi",
                    "transit_mode": "Taxi",
                    "cost_pct": 0.30,
                },
            },
            {
                "theme": "Suburban Energy, Bandra Hipster Vibe & Bollywood Seaside",
                "summary": "Cross the engineering marvel of the Sea Link to explore Bandra's colonial Portuguese villages, seaside rocks, and trendy cafes.",
                "morning": {
                    "title": "Bandra-Worli Sea Link Drive & Mount Mary Basilica",
                    "description": "Glide over the Arabian Sea across the cable-stayed Sea Link bridge. Climb up to the 16th-century Mount Mary Church overlooking the sea, followed by a walk through the charming painted lanes of Ranwar Village.",
                    "location": "Bandra West, Mount Mary",
                    "category": "Coastal Drive & Heritage",
                    "neighborhood": "Bandra West Villages",
                    "transit_time": "25 mins cab across Sea Link",
                    "transit_mode": "Cab",
                    "cost_pct": 0.35,
                },
                "afternoon": {
                    "title": "Artisanal Bakeries at Pali Hill & Shopping on Linking Road",
                    "description": "Relax at chic celebrity-favorite cafes like Subko Coffee or Theobroma in Pali Hill. Hunt for affordable high-street fashion and Kolhapuri sandals along bustling Linking Road.",
                    "location": "Pali Hill & Linking Road, Bandra",
                    "category": "Shopping & Cafe Culture",
                    "neighborhood": "Pali Hill Suburban Quarter",
                    "transit_time": "10 mins auto-rickshaw",
                    "transit_mode": "Auto-rickshaw",
                    "cost_pct": 0.35,
                },
                "evening": {
                    "title": "Sea Breeze Walk at Bandra Bandstand & Juhu Beach Kulfi",
                    "description": "Walk along Bandstand promenade catching sea spray by Castella de Aguada (Bandra Fort) and catch a glimpse of Bollywood stars' residences. Wrap up with Malai Kulfi and Pav Bhaji at Juhu Beach.",
                    "location": "Bandra Bandstand & Juhu Beach",
                    "category": "Coastal Promenade & Street Food",
                    "neighborhood": "Bandra Coastline",
                    "transit_time": "15 mins auto-rickshaw",
                    "transit_mode": "Auto-rickshaw",
                    "cost_pct": 0.30,
                },
            },
        ],
    },
    "goa": {
        "city": "Goa",
        "state_country": "India",
        "tagline": "Sun, Sand, Portuguese Heritage & Susegad Coastal Living",
        "transit_types": ["Rented Scooter / Bike", "Goa Miles Taxi", "Private Car Hire", "Ferry"],
        "local_specialties": ["Goan Fish Curry Thali", "Poi with Chorizo", "Prawn Balchão", "Bebinca", "Feni Cocktail", "Xacuti"],
        "days": [
            {
                "theme": "Old Goa Cathedrals, Latin Quarter Pastel Mansions & Mandovi River",
                "summary": "Travel through time in Asia's former capital of Portuguese empire, walk through colorful Fontainhas, and cruise into the sunset.",
                "morning": {
                    "title": "Basilica of Bom Jesus (UNESCO) & Se Cathedral in Old Goa",
                    "description": "Stand beneath the baroque golden altars of Se Cathedral and pay respects at the sacred reliquary of St. Francis Xavier inside the 16th-century Basilica of Bom Jesus.",
                    "location": "Old Goa (Velha Goa)",
                    "category": "UNESCO Heritage Churches",
                    "neighborhood": "Old Goa Historic Enclave",
                    "transit_time": "15 mins drive from Panaji",
                    "transit_mode": "Scooter / Cab",
                    "cost_pct": 0.25,
                },
                "afternoon": {
                    "title": "Fontainhas Latin Quarter Pastel Walk & Authentic Goan Fish Thali",
                    "description": "Wander among vivid ochre, indigo, and terracotta Portuguese-era villas with oyster-shell windows in Fontainhas. Relish a kingfish rawa fry thali with sol kadhi at heritage restaurant Viva Panjim.",
                    "location": "Fontainhas, Panaji",
                    "category": "Heritage Walk & Culinary",
                    "neighborhood": "Panaji Latin Quarter",
                    "transit_time": "10 mins drive",
                    "transit_mode": "Cab",
                    "cost_pct": 0.40,
                },
                "evening": {
                    "title": "Sunset Cruise along Mandovi River & Miramar Beach Walk",
                    "description": "Board a river catamaram along the Mandovi River with live Dekhni and Corridinho folk dancers. Watch dolphins breach as the sky turns crimson over the Arabian Sea mouth.",
                    "location": "Mandovi River Jetty, Panaji",
                    "category": "River Cruise & Sunset",
                    "neighborhood": "Panaji Waterfront",
                    "transit_time": "5 mins walk from Panaji",
                    "transit_mode": "Walk",
                    "cost_pct": 0.35,
                },
            },
            {
                "theme": "North Goa Cliffs, Golden Sands & Bohemian Beach Shacks",
                "summary": "Explore cliffside Portuguese forts, swim in turquoise waves, and relax at sun-kissed beach shacks with live acoustic music.",
                "morning": {
                    "title": "Aguada Fort, 17th-Century Lighthouse & Sinquerim Beach",
                    "description": "Explore the stone bastion of Fort Aguada constructed in 1612 to protect against Dutch invaders. Admire the panoramic 180-degree ocean view and old freshwater spring.",
                    "location": "Sinquerim / Candolim Coast",
                    "category": "Coastal Fortress",
                    "neighborhood": "Aguada Peninsula",
                    "transit_time": "20 mins via rented scooter",
                    "transit_mode": "Scooter",
                    "cost_pct": 0.30,
                },
                "afternoon": {
                    "title": "Anjuna Flea Market & Fresh Seafood Lunch by the Waves",
                    "description": "Browse bohemian dreamcatchers, leather crafts, and brass trinkets at Anjuna's iconic market. Sit on wooden benches at Curlies or Shiva Valley for butter-garlic calamari with chilled tender coconut water.",
                    "location": "Anjuna Beach Cliffs",
                    "category": "Beach Culture & Dining",
                    "neighborhood": "Anjuna Coastal Belt",
                    "transit_time": "15 mins scooter ride",
                    "transit_mode": "Scooter",
                    "cost_pct": 0.40,
                },
                "evening": {
                    "title": "Sunset at Chapora Fort (Dil Chahta Hai) & Vagator Cliff Lounge",
                    "description": "Climb up the red laterite ramparts of Chapora Fort overlooking the dramatic curve of Vagator Beach and the Ozran coastline. Finish with music and dinner at cliff-top lounge Thalassa or Antares.",
                    "location": "Chapora & Small Vagator Cliffs",
                    "category": "Scenic Sunset & Lounges",
                    "neighborhood": "Vagator Hill",
                    "transit_time": "10 mins ride",
                    "transit_mode": "Scooter",
                    "cost_pct": 0.30,
                },
            },
        ],
    },
    "paris": {
        "city": "Paris",
        "state_country": "France",
        "tagline": "The City of Light, Haute Couture & World-Class Gastronomy",
        "transit_types": ["Paris Métro", "RER Train", "Vélib' Bicycles", "Seine River Bateaux"],
        "local_specialties": ["Fresh Croissants & Café au Lait", "Steak Frites", "Duck Confit", "Ladurée Macarons", "Artisan Baguettes & French Cheeses"],
        "days": [
            {
                "theme": "Icons of Paris: Eiffel Tower, The Seine & Historic Latin Quarter",
                "summary": "Marvel at the iron lady, cruise down the Seine river beneath ornate stone bridges, and stroll historic university courtyards.",
                "morning": {
                    "title": "Sunrise at Trocadéro & Eiffel Tower Summit Ascension",
                    "description": "Capture postcard views of the Eiffel Tower from the Trocadéro terrace at sunrise. Ascend to the summit or 2nd floor for a breathtaking 360-degree panorama of Paris.",
                    "location": "Champ de Mars, 7th Arrondissement",
                    "category": "Iconic Monuments",
                    "neighborhood": "Eiffel Tower / Invalides",
                    "transit_time": "Métro Line 6 to Bir-Hakeim",
                    "transit_mode": "Paris Métro",
                    "cost_pct": 0.40,
                },
                "afternoon": {
                    "title": "Notre-Dame Cathedral, Sainte-Chapelle Stained Glass & Latin Quarter",
                    "description": "Marvel at the restored facade of Notre-Dame Cathedral on Île de la Cité and the 15 exquisite stained glass panels of Sainte-Chapelle. Grab a ham-and-brie baguette in the Latin Quarter.",
                    "location": "Île de la Cité & Latin Quarter",
                    "category": "Gothic Architecture & Walks",
                    "neighborhood": "Latin Quarter (5th Arr.)",
                    "transit_time": "12 mins via Métro Line 4",
                    "transit_mode": "Paris Métro",
                    "cost_pct": 0.30,
                },
                "evening": {
                    "title": "Golden Hour Seine River Cruise (Bateaux Mouches) & Bistro Dinner",
                    "description": "Board a glass-topped boat gliding along the Seine as riverbank monuments light up in gold. Dine at a traditional Parisian bistro with Steak Frites and warm chocolate fondant.",
                    "location": "Pont de l'Alma & Saint-Germain-des-Prés",
                    "category": "Scenic Cruise & French Dining",
                    "neighborhood": "Saint-Germain (6th Arr.)",
                    "transit_time": "10 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.30,
                },
            },
            {
                "theme": "Masterpieces of the Louvre & Bohemian Montmartre",
                "summary": "Encounter the Mona Lisa in the world's greatest museum, followed by the winding cobblestone artist village of Montmartre.",
                "morning": {
                    "title": "Mona Lisa & Venus de Milo at the Grand Louvre Museum",
                    "description": "Enter through the glass pyramid to discover the winged Victory of Samothrace, Leonardo's Mona Lisa, and Napoleon III's lavish gilded apartments.",
                    "location": "Musée du Louvre, 1st Arrondissement",
                    "category": "World Heritage Museums",
                    "neighborhood": "Palais-Royal / Louvre",
                    "transit_time": "Métro Line 1 to Palais Royal",
                    "transit_mode": "Paris Métro",
                    "cost_pct": 0.45,
                },
                "afternoon": {
                    "title": "Tuileries Garden Walk & Hot Chocolate at Angelina",
                    "description": "Stroll down the manicured linden tree paths of Jardin des Tuileries towards Place de la Concorde. Indulge in velvety hot chocolate and Mont-Blanc pastry at famed tearoom Angelina.",
                    "location": "Rue de Rivoli & Jardin des Tuileries",
                    "category": "Gardens & Patisserie",
                    "neighborhood": "Concorde / Tuileries",
                    "transit_time": "5 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.25,
                },
                "evening": {
                    "title": "Sunset from Sacré-Cœur Basilica & Artists of Place du Tertre",
                    "description": "Climb the funicular to Montmartre's crowning white-domed basilica. Watch street painters create caricatures in Place du Tertre and enjoy French onion soup at a candlelit terrace.",
                    "location": "Sacré-Cœur, Montmartre, 18th Arr.",
                    "category": "Hilltop Views & Bohemian Dining",
                    "neighborhood": "Montmartre",
                    "transit_time": "18 mins via Métro Line 12 to Abbesses",
                    "transit_mode": "Paris Métro",
                    "cost_pct": 0.30,
                },
            },
        ],
    },
    "tokyo": {
        "city": "Tokyo",
        "state_country": "Japan",
        "tagline": "Futuristic Metropolis where Ancient Tradition Meets High-Tech Wonder",
        "transit_types": ["JR Yamanote Line", "Tokyo Metro / Toei Subway", "Suica / Pasmo IC Card", "Walking"],
        "local_specialties": ["Tonkotsu Ramen at Ichiran", "Tsukiji Fresh Nigiri Sushi", "Yakitori skewers", "Matcha soft serve", "Takoyaki", "Wagyu Teppanyaki"],
        "days": [
            {
                "theme": "Old Edo Traditions & Futuristic Shibuya Crossing",
                "summary": "From the oldest Buddhist temple in Tokyo to the kinetic neon energy of the world's busiest pedestrian crossing.",
                "morning": {
                    "title": "Sensō-ji Buddhist Temple & Nakamise-dori Street Food in Asakusa",
                    "description": "Pass beneath the giant red Kaminarimon lantern into Sensō-ji, Tokyo's oldest temple founded in 628 AD. Sample melonpan sweet buns and freshly grilled Ningyo-yaki cakes along the temple street.",
                    "location": "Asakusa, Taito City",
                    "category": "Ancient Temples & Culture",
                    "neighborhood": "Asakusa Historic District",
                    "transit_time": "Ginza Line to Asakusa",
                    "transit_mode": "Tokyo Metro",
                    "cost_pct": 0.25,
                },
                "afternoon": {
                    "title": "Meiji Jingu Shinto Shrine Forest & Harajuku Takeshita Street",
                    "description": "Walk beneath towering cedar Torii gates into the tranquil Meiji Shrine. Exit directly into Harajuku's Takeshita Street, a vibrant alley of kawaii fashion, animal cafes, and giant cotton candy.",
                    "location": "Yoyogi Park & Harajuku, Shibuya",
                    "category": "Shinto Shrines & Youth Culture",
                    "neighborhood": "Harajuku & Yoyogi",
                    "transit_time": "JR Yamanote Line to Harajuku",
                    "transit_mode": "JR Yamanote Line",
                    "cost_pct": 0.35,
                },
                "evening": {
                    "title": "World-Famous Shibuya Scramble Crossing & Hachiko Statue",
                    "description": "Experience the surge of up to 3,000 people crossing simultaneously at Shibuya Crossing. Head up to Shibuya Sky observation deck for neon sunset vistas, followed by piping hot ramen.",
                    "location": "Shibuya Station & Shibuya Sky",
                    "category": "Neon Cityscapes & Nightlife",
                    "neighborhood": "Shibuya City Core",
                    "transit_time": "1 stop on Yamanote Line (3 mins)",
                    "transit_mode": "JR Yamanote Line",
                    "cost_pct": 0.40,
                },
            },
        ],
    },
    "lisbon": {
        "city": "Lisbon",
        "state_country": "Portugal",
        "tagline": "City of Seven Hills, Fado Melodies & Golden Atlantic Light",
        "transit_types": ["Historic Tram 28", "Lisbon Metro", "Santa Justa Lift", "Ferry across Tagus"],
        "local_specialties": ["Pastéis de Belém (Custard Tarts)", "Bacalhau à Brás (Salt Cod)", "Bifana pork sandwich", "Ginjinha cherry liqueur", "Grilled Sardines"],
        "days": [
            {
                "theme": "Historic Alfama Miradouros, Tram 28 & Fado Heritage",
                "summary": "Ride the iconic yellow vintage tram up Lisbon's oldest cobblestone hill and listen to soulful Fado music.",
                "morning": {
                    "title": "Vintage Tram 28 & Panoramic Miradouro de Santa Luzia",
                    "description": "Rumble up the steep hills on wood-paneled Tram 28. Step off at Miradouro de Santa Luzia for sweeping vistas over terracotta roofs and the glittering Tagus estuary with vibrant bougainvillea.",
                    "location": "Alfama Hill, Lisbon",
                    "category": "Historic Transit & Panoramas",
                    "neighborhood": "Alfama Moorish Quarter",
                    "transit_time": "Tram 28 ride",
                    "transit_mode": "Historic Tram",
                    "cost_pct": 0.25,
                },
                "afternoon": {
                    "title": "São Jorge Moorish Castle & Time Out Market Feasting",
                    "description": "Walk along the fortified battlements of Castelo de São Jorge with peacocks roaming olive groves. Descend to Time Out Market in Cais do Sodré to taste gourmet dishes from Portugal's Michelin-starred chefs.",
                    "location": "Castelo & Mercado da Ribeira",
                    "category": "Medieval Forts & Gastronomy",
                    "neighborhood": "Baixa & Cais do Sodré",
                    "transit_time": "15 mins walk / funicular",
                    "transit_mode": "Walk",
                    "cost_pct": 0.45,
                },
                "evening": {
                    "title": "Candlelit Traditional Fado Dinner in Bairro Alto",
                    "description": "As dusk falls, wander the lively bohemian lanes of Bairro Alto. Savor fresh grilled cod (Bacalhau) paired with crisp Vinho Verde while a local singer and 12-string Portuguese guitar perform emotional Fado.",
                    "location": "Bairro Alto & Chiado",
                    "category": "Cultural Music & Dining",
                    "neighborhood": "Bairro Alto",
                    "transit_time": "8 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.30,
                },
            },
            {
                "theme": "Age of Discoveries in Belém & Warm Custard Tarts",
                "summary": "Witness Manueline architectural wonders on the riverfront and taste the original secret-recipe pastéis.",
                "morning": {
                    "title": "Jerónimos Monastery (UNESCO) & Monument to the Discoveries",
                    "description": "Marvel at the intricate stone carved cloister columns resembling coral and ropes at Mosteiro dos Jerónimos, where explorer Vasco da Gama is entombed. Walk along the river to the Padrão dos Descobrimentos.",
                    "location": "Praça do Império, Belém",
                    "category": "UNESCO World Heritage",
                    "neighborhood": "Belém Waterfront",
                    "transit_time": "Tram 15E from Praça da Figueira",
                    "transit_mode": "Tram 15E",
                    "cost_pct": 0.35,
                },
                "afternoon": {
                    "title": "Pastéis de Belém Bakery & Belém Fortified Tower",
                    "description": "Indulge in warm egg custard tarts dusted with cinnamon at the original Fábrica de Pastéis de Belém (baking since 1837). Continue to the fairytale 16th-century Belém Tower guarding the Tagus estuary.",
                    "location": "Rua de Belém & Torre de Belém",
                    "category": "Culinary Heritage & Fortresses",
                    "neighborhood": "Belém Maritime Quarter",
                    "transit_time": "10 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.35,
                },
                "evening": {
                    "title": "Sunset Cocktails at Miradouro de São Pedro de Alcântara",
                    "description": "Take the Glória Funicular up to São Pedro de Alcântara viewpoint garden. Sip port wine spritzers while overlooking the illuminated castle hill across the valley.",
                    "location": "Miradouro de São Pedro de Alcântara",
                    "category": "Viewpoints & Evening Ambiance",
                    "neighborhood": "Príncipe Real",
                    "transit_time": "Tram back to Chiado",
                    "transit_mode": "Tram",
                    "cost_pct": 0.30,
                },
            },
            {
                "theme": "Modern Lisbon, Oceanarium & Tagus Waterfront",
                "summary": "Discover the futuristic architecture of Parque das Nações, Europe's finest aquarium, and riverside dining.",
                "morning": {
                    "title": "Oceanário de Lisboa (Global Marine Habitats)",
                    "description": "Visit Europe's largest indoor aquarium situated in a floating pavilion on the Tagus dock, featuring sea otters, giant sunfish, penguins, and manta rays in an enormous central tank.",
                    "location": "Parque das Nações",
                    "category": "Marine Biology & Family",
                    "neighborhood": "Parque das Nações",
                    "transit_time": "Red Line Metro to Oriente",
                    "transit_mode": "Lisbon Metro",
                    "cost_pct": 0.40,
                },
                "afternoon": {
                    "title": "Telecabine Cable Car & Calatrava's Gare do Oriente",
                    "description": "Glide above the river on the Telecabine cable car with views of the 17km Vasco da Gama Bridge. Admire architect Santiago Calatrava's futuristic palm-like glass arches at Oriente Station.",
                    "location": "Passeio das Tágides",
                    "category": "Modern Architecture & Views",
                    "neighborhood": "Oriente Waterfront",
                    "transit_time": "5 mins walk",
                    "transit_mode": "Walk",
                    "cost_pct": 0.30,
                },
                "evening": {
                    "title": "Waterfront Dining & Sunset at Docas de Santo Amaro",
                    "description": "Dine under the towering red pillars of the 25 de Abril suspension bridge at Docas marina converted warehouses. Enjoy fresh seafood paella with Atlantic breezes.",
                    "location": "Docas de Santo Amaro Marina",
                    "category": "Marina Dining & Sunset",
                    "neighborhood": "Alcântara Docks",
                    "transit_time": "12 mins train / taxi",
                    "transit_mode": "Taxi",
                    "cost_pct": 0.30,
                },
            },
        ],
    },
}

# Additional destination-specific day plans extend the local catalog to four
# distinct days for each supported city. Opening times and seasonal access can
# change, so descriptions deliberately avoid promising a live schedule.
def _extra_day(theme: str, morning: tuple, afternoon: tuple, evening: tuple) -> Dict[str, Any]:
    def activity(item: tuple) -> Dict[str, Any]:
        title, description, location, category = item
        return {
            "title": title,
            "description": description,
            "location": location,
            "category": category,
            "neighborhood": location,
            "transit_time": "Check local route options",
            "transit_mode": "Local transit",
            "cost_pct": 0.33,
        }

    return {
        "theme": theme,
        "summary": f"A distinct local route focused on {theme.lower()}.",
        "morning": activity(morning),
        "afternoon": activity(afternoon),
        "evening": activity(evening),
    }


SUPPLEMENTAL_DESTINATION_DAYS: Dict[str, List[Dict[str, Any]]] = {
    "indore": [
        _extra_day("Museum collections and hilltop Jain heritage",
            ("Central Museum of Indore", "Explore regional sculpture, inscriptions, and archaeological collections; confirm current visitor hours before going.", "Central Museum, Residency", "Museum & History"),
            ("Gomatgiri Jain pilgrimage site", "Visit the hilltop Jain complex and its large Gomateshwara statue; dress respectfully and plan transport for the out-of-center location.", "Gomatgiri, Airport Road", "Spiritual Heritage"),
            ("Pitra Parvat sunset viewpoint", "Take in the broad city and countryside outlook from this hilltop Hanuman site; check access and local conditions before the visit.", "Pitra Parvat, Bijasan Road", "Hilltop & Spiritual Sites")),
    ],
    "jaipur": [
        _extra_day("Royal memorials, printmaking, and modern marble architecture",
            ("Gaitore Royal Cenotaphs", "Walk among the carved marble and sandstone chhatris built as memorials for Jaipur's former rulers.", "Gaitore, Jaipur–Amber Road", "Royal Heritage"),
            ("Anokhi Museum of Hand Printing", "Learn how block printing is practiced and preserved through tools, textiles, and demonstrations; verify the museum's current schedule.", "Anokhi Museum, Amber", "Craft & Design"),
            ("Birla Temple after dusk", "See the white-marble Lakshmi-Narayan temple and its detailed carvings; observe local customs and check visiting hours.", "Birla Temple, Moti Dungari", "Temple Architecture")),
    ],
    "delhi": [
        _extra_day("Central museums, memorials, and garden tombs",
            ("National Museum galleries", "Explore collections spanning Indian art, archaeology, and cultural history; check current exhibitions and opening hours.", "National Museum, Janpath", "Museum & History"),
            ("Safdarjung's Tomb", "Walk through the late Mughal garden-tomb complex and notice its architecture and landscaped setting.", "Safdarjung's Tomb, Lodhi Road", "Monument & Gardens"),
            ("Lodhi-era neighborhood dinner", "Choose a locally reviewed restaurant around the Lodhi Road or Khan Market area after an evening garden walk.", "Lodhi Road and Khan Market", "Neighborhood Dining")),
        _extra_day("Craft traditions, old fortifications, and public gardens",
            ("National Crafts Museum", "Browse craft traditions and regional objects in the museum's galleries; check for current demonstrations before visiting.", "National Crafts Museum, Pragati Maidan", "Craft & Culture"),
            ("Purana Qila ramparts and grounds", "Explore the old fort complex and its open grounds, allowing time for the museum or lake area if open.", "Purana Qila, Mathura Road", "Fort & Archaeology"),
            ("Sunder Nursery evening stroll", "Unwind among restored heritage structures, gardens, and planted landscapes; verify seasonal hours and entry details.", "Sunder Nursery, Nizamuddin", "Garden & Heritage")),
    ],
    "mumbai": [
        _extra_day("Island caves, city collections, and Colaba street life",
            ("Elephanta Caves", "Take the ferry from the Gateway of India to explore the island's rock-cut cave art; check ferry operation, entry details, and the weekly closure before travel.", "Elephanta Island, Mumbai Harbour", "Rock-cut Heritage"),
            ("Chhatrapati Shivaji Maharaj Vastu Sangrahalaya", "Explore art, archaeology, and natural-history collections in the museum near the Fort district.", "CSMVS, Fort", "Museum & Art"),
            ("Colaba Causeway evening walk", "Browse the lively shopping street and choose dinner in the Colaba neighborhood.", "Colaba Causeway", "Markets & Dining")),
        _extra_day("Kanheri's cave heritage and Mumbai's green north",
            ("Sanjay Gandhi National Park", "Spend the morning in the city's large protected green space; check entry rules and transport options ahead of time.", "Sanjay Gandhi National Park, Borivali", "Nature & Outdoors"),
            ("Kanheri Caves", "Explore the Buddhist cave complex within the park and its rock-cut architecture; allow time for the park journey.", "Kanheri Caves, Borivali", "Buddhist Heritage"),
            ("Bandra fort and seafront", "Walk the historic Bandra fort area and nearby promenade for open views across the coast.", "Bandra Fort and Bandstand", "Coastal Walk")),
    ],
    "goa": [
        _extra_day("Island villages, ferry crossings, and birdlife",
            ("Divar Island village loop", "Take a local ferry crossing and explore the island's quiet lanes and village scenery; verify ferry times before setting out.", "Divar Island, via Ribandar", "Island & Village Life"),
            ("Dr. Salim Ali Bird Sanctuary", "Look for wetland and mangrove birdlife on Chorao Island; bring sun protection and check access conditions.", "Chorao Island, Mandovi estuary", "Birdlife & Nature"),
            ("Ribandar riverside sunset", "Return toward Ribandar for a relaxed riverside evening and a meal featuring Goan specialties.", "Ribandar, Mandovi River", "Riverside & Local Food")),
        _extra_day("South Goa's quieter coast and inland spice traditions",
            ("Cabo de Rama Fort", "Explore the coastal fort ruins and sea-facing viewpoints; arrange transport in advance and check local access.", "Cabo de Rama, Canacona", "Coastal Heritage"),
            ("South Goa village and spice garden visit", "Choose a currently operating local spice farm or village experience and confirm reservations, transport, and meal inclusions directly.", "Ponda hinterland", "Food & Agriculture"),
            ("Palolem shoreline evening", "Take a gentle coastal walk and enjoy dinner from a licensed local restaurant; follow beach and swimming safety notices.", "Palolem, Canacona", "Beach & Dining")),
    ],
    "paris": [
        _extra_day("Left Bank art, gardens, and literary cafés",
            ("Musée d'Orsay", "Explore the museum's 19th-century art collection inside the former railway station; book ahead and check current opening days.", "Musée d'Orsay, Left Bank", "Art Museum"),
            ("Luxembourg Gardens", "Walk the formal gardens, tree-lined paths, and open lawns around the Luxembourg Palace.", "Jardin du Luxembourg, 6th arrondissement", "Garden & Leisure"),
            ("Saint-Germain-des-Prés café evening", "Choose a café or small restaurant around Saint-Germain-des-Prés and enjoy an unhurried Left Bank evening.", "Saint-Germain-des-Prés", "Neighborhood Dining")),
        _extra_day("Canal-side streets, local markets, and Père-Lachaise",
            ("Canal Saint-Martin walk", "Follow the canal-side footpaths, bridges, and waterside cafés; keep to public paths and check current event access.", "Canal Saint-Martin, 10th arrondissement", "Canal & Neighborhood Walk"),
            ("Marché des Enfants Rouges", "Browse Paris's historic covered market and choose a casual lunch from its food stalls; verify current market hours.", "Marché des Enfants Rouges, Marais", "Market & Food"),
            ("Père-Lachaise cemetery walk", "Explore the cemetery's public paths and historic memorials respectfully; use the official map and check access hours.", "Père-Lachaise, 20th arrondissement", "History & Gardens")),
    ],
    "tokyo": [
        _extra_day("Ueno museums, pond paths, and market stalls",
            ("Tokyo National Museum", "Explore Japanese and Asian art collections in Ueno Park; check exhibition details and opening days.", "Tokyo National Museum, Ueno Park", "Museum & Art"),
            ("Shinobazu Pond and Ueno Park", "Walk the pond paths and park grounds, with time for a seasonal stop at a nearby museum or shrine.", "Shinobazu Pond, Ueno", "Park & Nature"),
            ("Ameyoko market food walk", "Browse the busy market lanes under the railway and try a few casual local snacks.", "Ameyoko, Ueno–Okachimachi", "Market & Street Food")),
        _extra_day("Yanaka lanes, temple district, and old-town cafés",
            ("Nezu Shrine grounds", "Visit the shrine grounds and walk the surrounding traditional neighborhood; check seasonal access notes.", "Nezu Shrine, Bunkyo", "Shrine & Culture"),
            ("Yanaka Ginza shopping street", "Explore the compact shopping street for everyday snacks, small shops, and neighborhood life.", "Yanaka Ginza, Yanaka", "Neighborhood & Food"),
            ("Yanaka backstreet café evening", "Finish with a quiet café or small local restaurant in Yanaka and plan the return via nearby rail stations.", "Yanaka, Taito", "Local Dining")),
        _extra_day("Kichijoji parkside calm and western Tokyo culture",
            ("Inokashira Park", "Take an easy walk around the park's ponds and tree-lined paths; boat rentals and seasonal scenery vary.", "Inokashira Park, Kichijoji", "Park & Outdoors"),
            ("Ghibli Museum or Kichijoji galleries", "If you secure advance admission, visit the Ghibli Museum; otherwise choose a local gallery or shop street nearby.", "Mitaka and Kichijoji", "Museum & Arts"),
            ("Harmonica Yokocho dinner", "Explore the narrow alley dining area for small eateries and a lively local-food evening.", "Harmonica Yokocho, Kichijoji", "Food & Nightlife")),
    ],
    "lisbon": [
        _extra_day("Ajuda's botanical gardens and creative west-side Lisbon",
            ("Ajuda Botanical Garden", "Walk Portugal's historic botanical garden and its formal terraces; verify current opening hours and entrance details.", "Jardim Botânico da Ajuda, Ajuda", "Garden & Nature"),
            ("Ajuda and Belém neighborhood museums", "Choose a nearby palace or museum that is open on the day and explore the quieter Ajuda streets between stops.", "Ajuda, western Lisbon", "Culture & Museums"),
            ("LX Factory food and design evening", "Browse the converted industrial complex's shops and eateries; check which venues and events are open that evening.", "LX Factory, Alcântara", "Food, Design & Nightlife")),
    ],
}


# Helper to find matching destination profile
def find_curated_destination(dest_input: str) -> Optional[Dict[str, Any]]:
    clean = re.sub(r"[^a-zA-Z\s]", "", dest_input.lower()).strip()
    for key, data in DESTINATION_DATABASE.items():
        if key in clean or clean in key or data["city"].lower() in clean:
            profile = dict(data)
            profile["days"] = [*data.get("days", []), *SUPPLEMENTAL_DESTINATION_DAYS.get(key, [])]
            return profile
    return None


def generate_smart_procedural_day(
    destination: str,
    day_number: int,
    travel_style: str = "cultural",
    interests: Optional[List[str]] = None,
    budget_per_day: float = 5000.0,
    currency: str = "INR",
    dietary_needs: Optional[str] = None,
    pace: str = "moderate",
    destination_profile: Optional[Dict[str, Any]] = None,
    used_activity_titles: Optional[set[str]] = None,
) -> Dict[str, Any]:
    """Generates authentic, high-quality distinct activities for any global destination."""
    dest = destination.strip().title()
    style = (travel_style or "cultural").lower()
    interests = interests or ["Culture & Sights", "Gastronomy"]
    first_interest = interests[0] if interests else "Heritage"
    second_interest = interests[1] if len(interests) > 1 else "Local Cuisine"

    profile = destination_profile or {}
    city = profile.get("city", dest)
    specialties = profile.get("local_specialties") or []
    used_activity_titles = used_activity_titles if used_activity_titles is not None else set()
    curated_activities = [
        item
        for day in profile.get("days", [])
        for slot in ("morning", "afternoon", "evening")
        if (item := day.get(slot))
    ]

    def best_curated_item(
        keywords: List[str],
        used: Optional[set[str]] = None,
        candidates: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        used = used if used is not None else set()
        ranked = []
        items = candidates if candidates is not None else curated_activities
        for item in items:
            title = item.get("title", "")
            if title in used:
                continue
            text = " ".join((title, item.get("description", ""), item.get("category", ""))).lower()
            score = sum(1 for keyword in keywords if keyword in text)
            ranked.append((score, item))
        ranked.sort(key=lambda pair: pair[0], reverse=True)
        if not ranked or not ranked[0][0]:
            return None
        cutoff = max(1, ranked[0][0] - 1)
        candidates = [item for score, item in ranked if score >= cutoff]
        selected = candidates[(day_number - 1 + seed % len(candidates)) % len(candidates)]
        used.add(selected["title"])
        used_activity_titles.add(selected["title"])
        return selected

    interest_text = " ".join(interests).lower()
    food_focus = style == "foodie" or any(term in interest_text for term in ("food", "cuisine", "gastronomy", "culinary"))
    nightlife_focus = style == "nightlife" or any(term in interest_text for term in ("nightlife", "night life", "lounge", "live music"))
    history_focus = style in ("cultural", "sightseeing") or any(term in interest_text for term in ("history", "heritage", "architecture", "museum", "art"))

    # Seed variation with preferences so each travel style gets its own plan.
    seed = int(hashlib.md5(f"{city}-{day_number}-{style}-{'|'.join(interests)}".encode()).hexdigest()[:8], 16)

    # Detect region / environment for realistic landmarks and transport
    is_indian = any(sub in dest.lower() for sub in ["india", "nagar", "pur", "bad", "garh", "pradesh", "karnataka", "tamil", "bengal", "kerala", "gujarat", "bihar", "punjab", "shimla", "manali", "rishikesh", "varanasi", "amritsar", "kochi", "pune", "agra", "jaipur", "indore", "delhi", "mumbai", "goa", "udaipur", "bhopal", "gwalior", "jodhpur"])
    is_mountain = any(sub in dest.lower() for sub in ["manali", "shimla", "leh", "ladakh", "alps", "swiss", "himalaya", "nepal", "mussoorie", "nainital", "darjeeling", "gangtok", "queenstown", "innsbruck", "zermatt"])
    is_beach = any(sub in dest.lower() for sub in ["goa", "bali", "phuket", "beach", "island", "maldives", "hawaii", "cancun", "ibiza", "santorini", "pattaya", "krabi", "bora", "miami"])

    if is_mountain:
        transit_modes = ["Mountain 4x4 Cab", "Ropeway / Cable Car", "Valley Trek Walk", "Shared Hill Taxi"]
        morning_loc = f"{dest} Upper Ridge & Mountain Lookout"
        morning_act = f"Sunrise Panoramic Trek across {dest} Valley & Himalayan Viewpoint"
        morning_desc = f"Catch the dawn mist clearing over the peaks. Enjoy hot ginger tea at cliffside wooden kiosks and explore historic cedar trails focusing on {first_interest}."
        afternoon_loc = f"{dest} Old Mountain Village & Stream Bank"
        afternoon_act = f"Alpine Forest Walk & Organic Riverside Cafe Dining"
        afternoon_desc = f"Hike down to the glacial stream. Savor hearty local mountain bread, seasonal stews, and herbal teas while relaxing by crystal waters."
        evening_loc = f"{dest} Mall Road & Tibetan / Folk Crafts Market"
        evening_act = f"Stroll {dest} Timber Promenade & Twilight Campfire Chill"
        evening_desc = f"Explore handcrafted woolens, pine crafts, and piping hot dumplings at the illuminated town square."
    elif is_beach:
        transit_modes = ["Rented Scooter / Moped", "Beachside Tuk-tuk", "Coastal Cab", "Speedboat / Ferry"]
        morning_loc = f"{dest} Coastal Cove & Cliffs"
        morning_act = f"Early Morning Tide Walk & Sea Caves Exploration"
        morning_desc = f"Take advantage of gentle morning breezes along {dest}'s shoreline. Watch local fishermen bring in the morning catch and discover hidden tidal pools."
        afternoon_loc = f"{dest} Seaside Village & Pier"
        afternoon_act = f"Waterfront Seafood Shack & Handcrafted Coral Bazaar"
        afternoon_desc = f"Relax under thatched palm canopies with fresh grilled catch, tropical coconut coolers, and artisanal shell crafts."
        evening_loc = f"{dest} Sunset Beach & Cliffside Lounge"
        evening_act = f"Crimson Sunset Horizon & Fire-lit Acoustic Beach Vibes"
        evening_desc = f"Watch the sun plunge into the ocean waves while enjoying tropical mocktails, seafood appetizers, and acoustic lounge music."
    elif is_indian:
        transit_modes = ["E-Rickshaw", "Auto-rickshaw", "Metro / City Rail", "App Cab"]
        districts = [f"{dest} Old Fort & Walled City", f"{dest} Lake Promenade & Civic Park", f"{dest} Temple & Artisan Guild", f"{dest} Royal Palace Precinct", f"{dest} Bazaar & Silk Market"]
        cur_district = districts[(day_number - 1 + (seed % 2)) % len(districts)]
        morning_loc = f"{cur_district}"
        morning_act = f"Heritage Citadel & Architecture Walk in {dest}"
        morning_desc = f"Start early with traditional breakfast delicacies at historic halwai stalls. Tour centuries-old carved stone pavilions, learning about the rich founding heritage of {dest}."
        afternoon_loc = f"{dest} Central Handloom & Craft Guilds"
        afternoon_act = f"Artisan Workshops & Authentic Regional Thali Lunch"
        afternoon_desc = f"Visit master weavers, brass-smiths, and pottery artisans. Enjoy a leisurely regional thali lunch featuring seasonal dishes and hand-churned dairy treats."
        evening_loc = f"{dest} Vibrant Night Bazaar & Food Street"
        evening_act = f"Sensory Street Food Safari & Illuminated City Square"
        evening_desc = f"As temperatures cool, the historic street market comes alive with twinkling lights, spice aromas, and famous local evening chaats and sweets."
    else:
        transit_modes = ["City Metro / Subway", "Historic Tramway", "Walking Tour", "City Bus / Taxi"]
        districts = [f"{dest} Old Town Square", f"{dest} Arts & Museum Quarter", f"{dest} Riverfront / Harbor Canal", f"{dest} Historic Citadel & Gardens", f"{dest} Bohemian Latin District"]
        cur_district = districts[(day_number - 1 + (seed % 2)) % len(districts)]
        morning_loc = f"{cur_district}"
        morning_act = f"Architectural Discovery & Landmark Highlights of {dest}"
        morning_desc = f"Marvel at iconic civic monuments and historic facades. Stop at an artisanal bakery for fresh pastries and rich roast espresso before crowds gather."
        afternoon_loc = f"{dest} Cultural District & Covered Market"
        afternoon_act = f"Curated Art Galleries & Local Gastronomy Immersion"
        afternoon_desc = f"Explore renowned local exhibition halls and historic food markets. Taste artisan cheeses, seasonal regional specialties, and local delicacies."
        evening_loc = f"{dest} Riverfront Promenade & Old Quarter"
        evening_act = f"Twilight Stroll along Illuminated Bridges & Bistro Dinner"
        evening_desc = f"Relax as the historic streetlamps flicker to life. Enjoy dinner at a cozy neighborhood bistro pairing local dishes with warm evening ambiance."

    morning_category = "Heritage & Sights"
    afternoon_category = "Culinary & Crafts"
    evening_category = "Nightlife & Ambiance"
    curated_evenings = [day["evening"] for day in profile.get("days", []) if day.get("evening")]

    if style == "nightlife" or (style not in ("foodie", "cultural", "sightseeing") and nightlife_focus):
        morning_category, afternoon_category, evening_category = "Brunch & Leisure", "Arts & Evening Warm-up", "Nightlife & Live Music"
        brunch_options = ["a neighborhood bakery brunch", "a traditional tea-and-snack brunch", "a produce-market breakfast", "a slow café brunch"]
        breakfast = specialties[(day_number - 1) % len(specialties)] if specialties else brunch_options[(day_number - 1) % len(brunch_options)]
        daytime_options = [
            ("A creative-quarter gallery and café afternoon", "Browse independent galleries and design shops, then take a slow café break before the evening plans."),
            ("A market-lane wander and street-food warm-up", "Explore a lively market area in daylight, sampling a small local snack and saving room for later."),
            ("A live-arts district preview", "Look for a matinee, exhibition, or public performance, then take an early dinner close to tonight's venue."),
            ("A neighborhood music-history walk", "Explore local music venues and record shops while they are open, then plan a convenient route to the evening scene."),
        ]
        daytime_title, daytime_description = daytime_options[(day_number - 1) % len(daytime_options)]
        night_item = best_curated_item(
            ["night", "evening", "music", "bazaar", "market", "performance"],
            candidates=curated_evenings,
        )
        night_place = night_item.get("location", f"{city} evening district") if night_item else f"{city} evening district"
        morning_loc = f"{city} neighborhood cafes"
        morning_act = f"Slow-start brunch before a night out: {breakfast}"
        morning_desc = f"Keep the morning easy with a late start and a relaxed brunch featuring {breakfast}. Save energy for the evening and check local opening times before setting out."
        afternoon_loc = f"{city} arts and entertainment quarter"
        afternoon_act = f"{daytime_title} in {city}"
        afternoon_desc = daytime_description
        evening_loc = night_place
        night_fallbacks = ["Live music and a late set", "Night-market bites and people-watching", "A local performance and post-show drinks", "A relaxed lounge night with a DJ"]
        evening_act = night_item.get("title", f"{night_fallbacks[(day_number - 1) % len(night_fallbacks)]} in {city}") if night_item else f"{night_fallbacks[(day_number - 1) % len(night_fallbacks)]} in {city}"
        evening_desc = night_item.get("description", f"Make this the late-night highlight around {night_place}. Check tonight's schedule, opening hours, and safe transport options.") if night_item else f"Make this the late-night highlight around {night_place}. Check tonight's schedule, opening hours, and safe transport options."
    elif style == "foodie" or (style not in ("cultural", "sightseeing") and food_focus):
        morning_category, afternoon_category, evening_category = "Breakfast Tasting", "Food Market & Tasting", "Local Dining"
        fallback_breakfasts = ["a neighborhood bakery breakfast", "a traditional tea-and-snack stop", "a produce-market breakfast", "a slow café brunch"]
        fallback_tastings = ["seasonal market snacks", "regional breads and sweets", "fresh produce and street-food bites", "a small-plate neighborhood tasting"]
        fallback_dinners = ["a family-run regional kitchen", "a busy neighborhood food lane", "a modern local bistro", "a relaxed late supper near the evening quarter"]
        dish_a = specialties[(day_number - 1) % len(specialties)] if specialties else fallback_breakfasts[(day_number - 1) % len(fallback_breakfasts)]
        dish_b = specialties[(day_number + 1) % len(specialties)] if len(specialties) > 1 else fallback_tastings[(day_number - 1) % len(fallback_tastings)]
        food_item = best_curated_item(["breakfast", "food", "dining", "gastronomy", "cuisine", "market", "bazaar"])
        market_item = best_curated_item(["market", "bazaar", "food", "dining", "gastronomy", "cuisine"])
        evening_food = best_curated_item(["night", "dinner", "food", "dining", "gastronomy", "cuisine"])
        morning_loc = food_item.get("location", f"{city} breakfast quarter") if food_item else f"{city} breakfast quarter"
        morning_act = f"Local breakfast tasting: {dish_a}"
        morning_desc = f"Start with a guided tasting of {dish_a}. Try a small portion at a time, ask vendors how the dish is traditionally served, and leave room for the rest of the day's food stops."
        afternoon_loc = market_item.get("location", f"{city} market district") if market_item else f"{city} market district"
        afternoon_act = market_item.get("title", f"Market-to-table tasting: {dish_b}") if market_item else f"Market-to-table tasting: {dish_b}"
        afternoon_desc = market_item.get("description", f"Follow a compact market and neighborhood-food route, sampling {dish_b} alongside seasonal specialties. Keep the stops close together and pause for a relaxed lunch.") if market_item else f"Follow a compact market and neighborhood-food route, sampling {dish_b} alongside seasonal specialties. Keep the stops close together and pause for a relaxed lunch."
        evening_loc = evening_food.get("location", f"{city} dinner district") if evening_food else f"{city} dinner district"
        dinner_theme = fallback_dinners[(day_number - 1) % len(fallback_dinners)]
        evening_act = evening_food.get("title", f"Dinner at {dinner_theme}") if evening_food else f"Dinner at {dinner_theme}"
        evening_desc = evening_food.get("description", f"Finish with a relaxed meal at {dinner_theme}. Ask about seasonal dishes and check current service hours before you go.") if evening_food else f"Finish with a relaxed meal at {dinner_theme}. Ask about seasonal dishes and check current service hours before you go."
    elif history_focus:
        morning_category, afternoon_category = "History & Architecture", "Museums & Heritage"
        heritage_item = best_curated_item(["heritage", "historic", "history", "palace", "fort", "temple", "architecture", "museum"])
        already_selected = set(used_activity_titles)
        if heritage_item:
            already_selected.add(heritage_item["title"])
        second_heritage = best_curated_item(
            ["heritage", "historic", "history", "palace", "fort", "temple", "architecture", "museum", "art"],
            already_selected,
        )
        day_topics = [
            ("Origins and old-town lanes", "historic center", "museum and civic quarter", "Trace the city's growth through its public spaces, architecture, and neighborhood stories."),
            ("Markets and local makers", "traditional market district", "independent craft and shop lanes", "Explore working market streets, looking for crafts and everyday local life."),
            ("Parks and city viewpoints", "public garden or city park", "cultural collections quarter", "Balance museums with an unhurried outdoor walk and a viewpoint or public garden."),
            ("Living culture and neighborhood food", "contemporary neighborhood", "local arts and food quarter", "Spend time in a different neighborhood, connecting local traditions with its current food and arts scene."),
        ]
        day_topic, morning_area, afternoon_area, day_description = day_topics[(day_number - 1) % len(day_topics)]
        morning_loc = heritage_item.get("location", f"{city} {morning_area}") if heritage_item else f"{city} {morning_area}"
        morning_act = heritage_item.get("title", f"{day_topic}: a local walk in {city}") if heritage_item else f"{day_topic}: a local walk in {city}"
        morning_desc = heritage_item.get("description", day_description) if heritage_item else day_description
        afternoon_loc = second_heritage.get("location", f"{city} {afternoon_area}") if second_heritage else f"{city} {afternoon_area}"
        afternoon_act = second_heritage.get("title", f"{day_topic}: collections, makers, and local stories") if second_heritage else f"{day_topic}: collections, makers, and local stories"
        afternoon_desc = second_heritage.get("description", f"Use this afternoon to explore {day_topic.lower()} in {city}. Choose a museum, market, or community-run venue that fits the day's focus and check its opening hours.") if second_heritage else f"Use this afternoon to explore {day_topic.lower()} in {city}. Choose a museum, market, or community-run venue that fits the day's focus and check its opening hours."
        if food_focus and specialties:
            dish = specialties[(day_number - 1) % len(specialties)]
            afternoon_desc += f" Pause nearby to try a local favorite: {dish}."
        if nightlife_focus:
            night_item = best_curated_item(
                ["night", "evening", "music", "bazaar", "market", "performance"],
                candidates=curated_evenings,
            )
            evening_loc = night_item.get("location", f"{city} evening district") if night_item else f"{city} evening district"
            evening_act = f"After-dark music and performances in {city}"
            evening_desc = f"Keep the evening social after a history-focused day: find live music or a performance near {evening_loc}, check tonight's schedule, and plan a safe return."
            evening_category = "Live Music & Performance"
        elif food_focus:
            dish = specialties[(day_number - 1) % len(specialties)] if specialties else "regional specialties"
            evening_loc = f"{city} historic quarter"
            evening_act = f"Historic quarter twilight walk and a taste of {dish}"
            evening_desc = f"End with a relaxed walk through the historic quarter, then try {dish} at a nearby local restaurant. Check current service hours before you go."
            evening_category = "Heritage Walk & Dining"
        else:
            evening_loc = f"{city} historic quarter"
            evening_options = [
                ("Old-town twilight walk and regional dinner", "Notice how the historic streets change after dark, then choose a well-reviewed local restaurant nearby."),
                ("Market-lane evening and casual local supper", "Browse a different market street at a relaxed pace and try a seasonal specialty from a busy local stall."),
                ("Public garden sunset and neighborhood café", "Take a quiet outdoor break before dinner at a neighborhood café; check local closing times before setting out."),
                ("Live arts and a late neighborhood meal", "Look for a local performance or community arts event, then choose dinner close to the venue and arrange a safe ride back."),
            ]
            evening_title, evening_description = evening_options[(day_number - 1) % len(evening_options)]
            evening_act = f"{evening_title} in {city}"
            evening_desc = evening_description

        # Spend the destination's curated evening recommendations across the
        # trip before falling back to a general neighborhood suggestion.
        if curated_evenings and not food_focus and not nightlife_focus:
            evening_item = best_curated_item(
                ["night", "evening", "music", "market", "park", "sunset", "dining", "culture"],
                candidates=curated_evenings,
            )
            if evening_item:
                evening_loc = evening_item["location"]
                evening_act = evening_item["title"]
                evening_desc = evening_item["description"]
                evening_category = evening_item.get("category", "Evening Experience")

    elif curated_activities:
        # Styles such as adventure, relaxation, budget, and luxury should still
        # use real destination-specific stops instead of the same generic day.
        style_keywords = {
            "adventure": ["nature", "waterfall", "wildlife", "trail", "lake", "scenic", "outdoor", "adventure"],
            "relaxation": ["lake", "park", "garden", "sunset", "beach", "leisure", "relax", "scenic"],
            "budget": ["market", "bazaar", "walk", "street", "park", "food", "public"],
            "luxury": ["palace", "fine", "dining", "view", "heritage", "culture", "scenic"],
        }
        keywords = style_keywords.get(style, [])
        keywords += [word for word in re.findall(r"[a-z]{4,}", interest_text) if word not in keywords]
        first_stop = best_curated_item(keywords or ["heritage", "culture", "nature", "market"])
        second_stop = best_curated_item(keywords or ["food", "market", "architecture"])
        third_stop = best_curated_item(keywords or ["evening", "park", "dining"])
        if first_stop:
            morning_loc, morning_act, morning_desc = first_stop["location"], first_stop["title"], first_stop["description"]
            morning_category = first_stop.get("category", "Local Experience")
        if second_stop:
            afternoon_loc, afternoon_act, afternoon_desc = second_stop["location"], second_stop["title"], second_stop["description"]
            afternoon_category = second_stop.get("category", "Local Experience")
        if third_stop:
            evening_loc, evening_act, evening_desc = third_stop["location"], third_stop["title"], third_stop["description"]
            evening_category = third_stop.get("category", "Local Experience")

    diet_note = f" (Special attention given to {dietary_needs})" if dietary_needs else ""
    t_mode = transit_modes[(seed + day_number) % len(transit_modes)]

    activities = [
        {
            "time_slot": "Morning (08:30 - 12:00)",
            "title": morning_act,
            "description": morning_desc + diet_note,
            "location": morning_loc,
            "category": morning_category,
            "neighborhood": f"{dest} Heritage Core",
            "transit_time": "10-15 mins from hotel",
            "transit_mode": t_mode,
            "estimated_cost": round(budget_per_day * 0.30, 2),
        },
        {
            "time_slot": "Afternoon (12:30 - 16:30)",
            "title": afternoon_act,
            "description": afternoon_desc + diet_note,
            "location": afternoon_loc,
            "category": afternoon_category,
            "neighborhood": f"{dest} Cultural Quarter",
            "transit_time": "8-12 mins (geographically sequenced)",
            "transit_mode": "Walk / Short Ride",
            "estimated_cost": round(budget_per_day * 0.40, 2),
        },
    ]

    if pace in ["moderate", "fast", "fast-paced"] or style == "nightlife":
        activities.append({
            "time_slot": "Evening (17:30 - 21:30)",
            "title": evening_act,
            "description": evening_desc,
            "location": evening_loc,
            "category": evening_category,
            "neighborhood": f"{dest} Evening Hub",
            "transit_time": "12-15 mins via " + t_mode,
            "transit_mode": t_mode,
            "estimated_cost": round(budget_per_day * 0.30, 2),
        })

    theme_styles = {
        "cultural": "Culture & local stories",
        "foodie": "Food & local flavors",
        "adventure": "Outdoor discovery",
        "beach": "Coastal escape",
        "tropical": "Nature & green spaces",
        "sightseeing": "City highlights",
        "nightlife": "After-dark experiences",
        "relaxation": "A slower day",
    }
    day_theme = theme_styles.get(style, f"{style.capitalize()} experiences")
    title_location = evening_loc if style == "nightlife" else morning_loc
    day_title = f"Day {day_number}: {day_theme} around {title_location}"

    return {
        "day": day_number,
        "title": day_title,
        "summary": f"Explore {morning_loc} and {afternoon_loc}, with time for {first_interest.lower()} and {second_interest.lower()} along the way.",
        "activities": activities,
    }
