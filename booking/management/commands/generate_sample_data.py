from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import Hotel, Room
from decimal import Decimal
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    """
    Django management command to generate sample hotel and room data for the booking app using Faker.
    This command creates a specified number of hotels, each with a random number of rooms, and populates them with realistic data such as names, addresses, amenities, descriptions, images, and pricing. The data is tailored for Indian cities and includes a variety of hotel and room types, each with appropriate amenities and descriptions.
    Command-line arguments:
        --clear   : Clears existing Hotel and Room data before generating new data.
        --hotels  : Number of hotels to create (default: 20).
    Key Features:
    - Supports multiple Indian cities and popular areas within each city.
    - Generates unique hotel names, addresses, coordinates, and contact information.
    - Assigns hotel types (luxury, resort, boutique, mid_range, budget) with corresponding amenities and star ratings.
    - Creates rooms of various types (single, double, twin, suite, deluxe, family) with realistic amenities, sizes, and prices.
    - Uses hotel-related placeholder image URLs for hotels and rooms.
    - Produces detailed, context-aware descriptions for both hotels and rooms.
    - Outputs progress and summary of created hotels and rooms to the console.
    Intended for development and testing purposes to quickly populate the database with diverse and realistic sample data.
    """
    help = "Generate sample hotel and room data using Faker with hotel-related images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )
        parser.add_argument(
            "--hotels",
            type=int,
            default=20,
            help="Number of hotels to create (default: 20)",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Room.objects.all().delete()
            Hotel.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Hotel related data cleared."))

        self.create_hotels(options["hotels"])

        self.stdout.write(self.style.SUCCESS("Hotel data generation completed!"))

    def get_images(self, num_images=5):
        li = [
    "https://www.oberoihotels.com/images/oberoihotels/exotic-vacations/ev-video-thumb.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD45ICJU9KxXpr4EuhNrjO_tFgrpezSkWQAg&s",
    "https://r1imghtlak.mmtcdn.com/57663784996211e8bfae0adfcdb46c1c.jpg?&output-quality=75&downsize=910:612&crop=910:612;4,0&output-format=webp",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMPViRDgZCSyU7kynwklvUtxAHCxphfSR_Kg&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcPxDGd5KVzCqtypD-510Sn_6YXuoXg2uJpw&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSspeWsVDuveQ9dfAR1TfEISfgEmUmXUjy46g&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcK8s1RHx6Qo0Ie3ZVnyh_2ReXDuJ9y9r2Vg&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRggsXoPokAQijzp3q5MxbjwXQ0lD1xqL1Gdg&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcMk7JQ24Ga3pA9a2KKd6zdgMfLL5x-Xmaaw&s",
        ]
        images = []
        for I in range(num_images):
            value = random.randint(0, len(li)-1)
            images.append(li[value])
        # images = []   
        # for i in range(num_images):
        #     width = random.choice([800, 1024, 1200])
        #     height = random.choice([600, 768, 900])
        #     seed = random.randint(1, 1000)
            
        #     image_url = f"https://picsum.photos/{width}/{height}?random={random.randint(0, seed)}-{seed}"
        #     images.append(image_url)
        
        return images

    def get_hotel_description(self, hotel_type, city, area, amenities):
        """Generate realistic hotel descriptions based on type and amenities"""

        base_descriptions = {
            "luxury": [
                f"Experience unparalleled luxury at our exquisite hotel in the heart of {area}, {city}. Our elegantly appointed accommodations feature world-class amenities and personalized service that exceeds expectations.",
                f"Discover the epitome of sophistication and comfort at our premium luxury hotel in {area}. With breathtaking views and exceptional facilities, we offer an unforgettable stay in {city}.",
                f"Indulge in the finest hospitality at our luxury retreat in {area}, {city}. From opulent suites to award-winning dining, every detail is crafted for the discerning traveler.",
                f"Welcome to our prestigious luxury hotel in {area}, where timeless elegance meets modern sophistication. Experience {city}'s finest hospitality with our world-class service.",
                f"Immerse yourself in luxury at our five-star hotel in {area}. Our meticulously designed spaces and exceptional amenities create an oasis of comfort in bustling {city}.",
                f"Step into a world of refined luxury at our premier hotel in {area}, {city}. Every moment of your stay is enhanced by our attention to detail and commitment to excellence.",
                f"Our luxury hotel in {area} redefines hospitality with its blend of contemporary design and classic elegance, offering an extraordinary experience in {city}.",
                f"Experience the pinnacle of luxury hospitality at our distinguished hotel in {area}. From personalized service to exquisite amenities, we create unforgettable memories in {city}.",
            ],
            "resort": [
                f"Escape to our stunning resort in {area}, {city}, where relaxation meets adventure. Enjoy world-class facilities, beautiful surroundings, and exceptional service in a tranquil setting.",
                f"Welcome to our premier resort destination in {area}. Immerse yourself in luxury with our comprehensive recreational facilities and breathtaking natural beauty.",
                f"Experience the perfect getaway at our resort in {city}. With extensive amenities and activities for all ages, create lasting memories in our beautiful {area} location.",
                f"Discover paradise at our expansive resort in {area}, {city}. From rejuvenating spa treatments to exciting recreational activities, every day brings new adventures.",
                f"Nestled in the scenic {area} of {city}, our resort offers the perfect blend of relaxation and recreation. Enjoy pristine facilities and endless entertainment options.",
                f"Our resort in {area} is your gateway to the best of {city}. With luxurious accommodations and world-class amenities, every stay becomes a cherished vacation.",
                f"Experience resort living at its finest in {area}, {city}. Our comprehensive facilities and stunning location provide the ultimate escape from everyday life.",
                f"Welcome to our tropical paradise in {area}, where every sunrise brings new possibilities. Our resort in {city} offers the perfect blend of adventure and tranquility.",
            ],
            "boutique": [
                f"Discover our charming boutique hotel in the vibrant {area} district of {city}. Combining intimate luxury with personalized service, we offer a unique and memorable experience.",
                f"Experience distinctive style and character at our boutique property in {area}. Our thoughtfully designed spaces reflect the local culture and spirit of {city}.",
                f"Stay at our carefully curated boutique hotel in {area}, where every detail tells a story. Enjoy personalized attention and unique amenities in the heart of {city}.",
                f"Our boutique hotel in {area} captures the essence of {city} with its distinctive design and intimate atmosphere. Experience personalized luxury in a unique setting.",
                f"Immerse yourself in local culture at our boutique property in {area}. Each room tells a story, and every corner reflects the artistic spirit of {city}.",
                f"Experience boutique hospitality at its finest in {area}, {city}. Our individually designed spaces and personalized service create an intimate and memorable stay.",
                f"Our boutique hotel in {area} offers a refreshing alternative to conventional accommodations. Discover the charm and character that makes {city} special.",
                f"Step into our boutique sanctuary in {area}, where contemporary design meets local tradition. Experience the authentic spirit of {city} in luxurious comfort.",
            ],
            "mid_range": [
                f"Enjoy comfortable and convenient accommodation at our well-appointed hotel in {area}, {city}. We offer excellent value with modern amenities and friendly service.",
                f"Our centrally located hotel in {area} provides the perfect base for exploring {city}. With comfortable rooms and essential amenities, we ensure a pleasant stay.",
                f"Experience quality accommodation at our hotel in {area}. We combine comfort, convenience, and value to make your stay in {city} memorable.",
                f"Welcome to our comfortable hotel in {area}, {city}. Our modern facilities and warm hospitality ensure a pleasant and affordable stay for all travelers.",
                f"Our hotel in {area} offers the perfect balance of comfort and value. Enjoy modern amenities and convenient location while exploring beautiful {city}.",
                f"Stay comfortably at our well-equipped hotel in {area}. We provide all essential amenities and friendly service to make your {city} visit enjoyable and hassle-free.",
                f"Experience reliable comfort at our hotel in {area}, {city}. Our clean, modern rooms and helpful staff ensure a pleasant stay at an excellent value.",
                f"Our hotel in {area} combines modern comfort with traditional hospitality. Enjoy convenient amenities and warm service during your stay in {city}.",
            ],
            "budget": [
                f"Discover affordable comfort at our budget-friendly hotel in {area}, {city}. Clean, comfortable rooms with essential amenities ensure great value for money.",
                f"Stay smart at our economical hotel in {area}. We provide clean, comfortable accommodation with friendly service at unbeatable prices in {city}.",
                f"Our budget hotel in {area} offers simple, clean accommodation perfect for travelers seeking value in {city}. Essential amenities and warm hospitality guaranteed.",
                f"Experience affordable hospitality at our budget hotel in {area}, {city}. We offer clean, comfortable rooms and friendly service without breaking the bank.",
                f"Our economical hotel in {area} provides excellent value for budget-conscious travelers. Enjoy clean accommodations and essential amenities in {city}.",
                f"Stay affordably at our budget-friendly hotel in {area}. We offer clean, comfortable rooms and helpful service, making your {city} visit both pleasant and economical.",
                f"Our budget hotel in {area} proves that comfort doesn't have to be expensive. Enjoy clean rooms and friendly service at great prices in {city}.",
                f"Experience smart savings at our budget hotel in {area}, {city}. We provide clean, comfortable accommodation with all essential amenities at affordable rates.",
            ],
        }

        # Select base description
        description = random.choice(base_descriptions[hotel_type])

        # Add amenity-specific content
        amenity_descriptions = {
            "pool": "Take a refreshing dip in our sparkling swimming pool, perfect for relaxation after a day of exploration.",
            "spa": "Rejuvenate your body and mind at our full-service spa with therapeutic treatments and wellness programs.",
            "gym": "Maintain your fitness routine in our state-of-the-art fitness center equipped with modern exercise equipment.",
            "restaurant": "Savor exquisite cuisine at our on-site restaurant, featuring local specialties and international favorites.",
            "bar": "Unwind with premium beverages and signature cocktails at our stylish bar with a relaxed atmosphere.",
            "wifi": "Stay connected with complimentary high-speed Wi-Fi throughout the property, ensuring seamless connectivity.",
            "parking": "Enjoy the convenience of complimentary secure parking for all registered guests.",
            "business_center": "Conduct business seamlessly with our modern business center featuring printing, copying, and meeting facilities.",
            "conference_room": "Host successful meetings and events in our professional conference facilities with audio-visual equipment.",
            "room_service": "Indulge in 24-hour room service for ultimate convenience, with meals delivered directly to your room.",
            "concierge": "Our dedicated concierge team is available around the clock to assist with reservations, tours, and local recommendations.",
            "valet_parking": "Experience luxury with our professional valet parking service, ensuring your vehicle is well-cared for.",
            "kids_club": "Keep the little ones entertained at our supervised kids' club with age-appropriate activities and games.",
            "tennis_court": "Enjoy a game of tennis on our professional court with equipment rental available.",
            "golf_course": "Perfect your swing on our championship golf course designed by renowned architects.",
                        "beach_access": "Relax on pristine beaches just steps from your room, with complimentary beach chairs and umbrellas.",
            "shuttle_service": "Take advantage of our complimentary shuttle service to major attractions and transportation hubs.",
            "laundry": "Keep your wardrobe fresh with our professional laundry and dry cleaning services.",
            "pet_friendly": "Bring your furry friends along - we welcome pets with special amenities and services.",
        }

        # Add relevant amenity descriptions
        if amenities:
            selected_amenities = random.sample(amenities, min(2, len(amenities)))
            for amenity in selected_amenities:
                if amenity in amenity_descriptions:
                    description += f" {amenity_descriptions[amenity]}"

        return description

    def get_room_description(self, room_type, amenities, size_sqft):
        """Generate realistic room descriptions based on type and amenities"""
        
        base_descriptions = {
            "single": [
                f"Our comfortable single room is perfect for solo travelers seeking a cozy retreat. Thoughtfully designed with modern amenities and efficient use of space.",
                f"Enjoy a peaceful stay in our well-appointed single room, featuring contemporary furnishings and all essential amenities for a comfortable experience.",
                f"This charming single room offers the perfect sanctuary for individual guests, with modern comforts and a relaxing atmosphere.",
                f"Our single room combines comfort and functionality, providing everything needed for a pleasant solo stay with attention to detail.",
            ],
            "double": [
                f"Relax in our spacious double room featuring a comfortable queen-size bed and modern amenities for couples or business travelers.",
                f"Our elegantly furnished double room provides ample space and comfort with premium bedding and contemporary design elements.",
                f"Experience comfort and style in our double room, thoughtfully designed with modern amenities and a welcoming atmosphere.",
                f"This well-appointed double room offers the perfect blend of comfort and convenience for a memorable stay.",
            ],
            "twin": [
                f"Our twin room features two comfortable single beds, making it ideal for friends or colleagues traveling together.",
                f"Perfect for sharing, our twin room offers two separate beds with quality linens and modern amenities for a comfortable stay.",
                f"Enjoy the convenience of our twin room with two single beds, designed for travelers who prefer separate sleeping arrangements.",
                f"Our spacious twin room provides comfortable accommodation with two beds and all modern amenities for a pleasant stay.",
            ],
            "suite": [
                f"Indulge in luxury with our spacious suite featuring separate living and sleeping areas, premium amenities, and elegant furnishings.",
                f"Experience ultimate comfort in our expansive suite with distinct living spaces, upscale amenities, and sophisticated design.",
                f"Our luxurious suite offers generous space with separate areas for relaxation and rest, featuring premium amenities and elegant decor.",
                f"Enjoy the pinnacle of comfort in our suite, featuring spacious living areas, premium furnishings, and exceptional amenities.",
            ],
            "deluxe": [
                f"Our deluxe room offers enhanced comfort with premium amenities, elegant furnishings, and additional space for a truly luxurious experience.",
                f"Experience elevated comfort in our deluxe room, featuring upscale amenities, sophisticated design, and extra space for relaxation.",
                f"Indulge in our deluxe room with premium features, elegant decor, and enhanced amenities for a memorable and comfortable stay.",
                f"Our deluxe accommodation provides superior comfort with luxury amenities, stylish furnishings, and generous space.",
            ],
            "family": [
                f"Our spacious family room is designed to accommodate families comfortably, with multiple beds and family-friendly amenities.",
                f"Perfect for families, our large room features multiple sleeping arrangements and amenities designed with children in mind.",
                f"Enjoy quality family time in our generously sized room, equipped with multiple beds and thoughtful amenities for all ages.",
                f"Our family room provides ample space and comfort for families, with flexible sleeping arrangements and convenient amenities.",
            ],
        }

        description = random.choice(base_descriptions[room_type])
        
        # Add size information
        if size_sqft:
            description += f" The room spans {size_sqft} square feet, providing ample space for your comfort."

        # Add amenity-specific content
        amenity_descriptions = {
            "ac": "Climate-controlled air conditioning ensures your comfort year-round.",
            "tv": "Enjoy entertainment on the flat-screen TV with cable channels and streaming capabilities.",
            "wifi": "Stay connected with complimentary high-speed Wi-Fi throughout your stay.",
            "minibar": "Refresh yourself with beverages and snacks from the well-stocked minibar.",
            "balcony": "Step out onto your private balcony to enjoy fresh air and scenic views.",
            "jacuzzi": "Unwind in your private jacuzzi for the ultimate relaxation experience.",
            "kitchenette": "Prepare light meals and snacks in the convenient kitchenette with modern appliances.",
            "safe": "Keep your valuables secure in the in-room electronic safe.",
            "room_service": "Enjoy 24-hour room service for ultimate convenience and comfort.",
            "work_desk": "Stay productive at the spacious work desk with ergonomic seating and good lighting.",
            "coffee_maker": "Start your day right with fresh coffee from the in-room coffee maker.",
            "iron": "Keep your clothes wrinkle-free with the provided iron and ironing board.",
            "hair_dryer": "The ensuite bathroom includes a professional hair dryer for your convenience.",
            "bathtub": "Relax and rejuvenate in the luxurious bathtub after a long day.",
            "shower": "Refresh yourself in the modern walk-in shower with premium fixtures.",
        }

        # Add relevant amenity descriptions
        if amenities:
            selected_amenities = random.sample(amenities, min(3, len(amenities)))
            for amenity in selected_amenities:
                if amenity in amenity_descriptions:
                    description += f" {amenity_descriptions[amenity]}"

        return description

    def create_hotels(self, num_hotels):
        """Create sample hotels with rooms"""

        cities = [
            "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata",
            "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Goa",
            "Kochi", "Coimbatore", "Mysore", "Udaipur", "Agra",
            "Varanasi", "Rishikesh", "Manali", "Shimla", "Darjeeling"
        ]

        areas_by_city = {
            "Mumbai": ["Bandra", "Andheri", "Juhu", "Powai", "Colaba", "Marine Drive", "Worli", "Lower Parel"],
            "Delhi": ["Connaught Place", "Karol Bagh", "Paharganj", "Aerocity", "Hauz Khas", "Khan Market", "Lajpat Nagar"],
            "Bangalore": ["Koramangala", "Indiranagar", "Whitefield", "Electronic City", "MG Road", "Brigade Road", "Jayanagar"],
            "Chennai": ["T. Nagar", "Anna Nagar", "Adyar", "Velachery", "Mylapore", "Nungambakkam", "Besant Nagar"],
            "Kolkata": ["Park Street", "Salt Lake", "Howrah", "Ballygunge", "New Market", "Esplanade", "Alipore"],
            "Hyderabad": ["Banjara Hills", "Jubilee Hills", "Gachibowli", "Hitech City", "Secunderabad", "Begumpet", "Madhapur"],
            "Pune": ["Koregaon Park", "Viman Nagar", "Hinjewadi", "Kothrud", "Camp", "Deccan", "Aundh"],
            "Ahmedabad": ["Satellite", "Vastrapur", "Navrangpura", "Prahlad Nagar", "CG Road", "Maninagar", "Bopal"],
            "Jaipur": ["C-Scheme", "Malviya Nagar", "Vaishali Nagar", "Pink City", "MI Road", "Tonk Road", "Mansarovar"],
            "Goa": ["Calangute", "Baga", "Anjuna", "Panaji", "Candolim", "Arambol", "Palolem", "Vasco"],
            "Kochi": ["Marine Drive", "Fort Kochi", "Ernakulam", "Kakkanad", "Edappally", "Vytilla", "MG Road"],
            "Coimbatore": ["RS Puram", "Gandhipuram", "Race Course", "Saibaba Colony", "Peelamedu", "Singanallur"],
            "Mysore": ["Sayyaji Rao Road", "Chamundi Hills", "Jayalakshmipuram", "Kuvempunagar", "Hebbal", "Vijayanagar"],
            "Udaipur": ["City Palace", "Lake Pichola", "Fateh Sagar", "Sukhadia Circle", "Hiran Magri", "Sector 14"],
            "Agra": ["Taj Ganj", "Sadar Bazaar", "Civil Lines", "Dayalbagh", "Sikandra", "Fatehabad Road"],
            "Varanasi": ["Dashashwamedh Ghat", "Assi Ghat", "Godowlia", "Lanka", "Cantonment", "Sigra"],
            "Rishikesh": ["Laxman Jhula", "Ram Jhula", "Tapovan", "Swarg Ashram", "Muni Ki Reti", "Haridwar Road"],
            "Manali": ["Mall Road", "Old Manali", "Vashisht", "Solang Valley", "Hadimba", "Club House"],
            "Shimla": ["Mall Road", "Ridge", "Lakkar Bazaar", "Sanjauli", "Summer Hill", "Kufri Road"],
            "Darjeeling": ["Mall Road", "Chowrasta", "Happy Valley", "Lebong", "Jalapahar", "Observatory Hill"]
        }

        hotel_types = ["budget", "mid_range", "luxury", "resort", "boutique"]

        hotel_name_prefixes = [
            "Grand", "Royal", "Comfort", "Luxury", "Budget", "Premium", "City", "Garden", 
            "Ocean", "Mountain", "Heritage", "Modern", "Executive", "Family", "Business",
            "Boutique", "Classic", "Elite", "Golden", "Silver", "Crown", "Palace", "Manor",
            "Plaza", "Regency", "Imperial", "Majestic", "Serene", "Tranquil", "Elegant"
        ]

        hotel_name_suffixes = [
            "Hotel", "Inn", "Resort", "Suites", "Lodge", "Palace", "Residency", "Stay",
            "Retreat", "Manor", "Plaza", "Grand", "Towers", "Gardens", "Heights", "View",
            "Paradise", "Sanctuary", "Oasis", "Haven", "Escape", "Hideaway"
        ]

        amenities_by_type = {
            "luxury": [
                ["wifi", "pool", "spa", "gym", "restaurant", "bar", "room_service", "concierge", "valet_parking"],
                ["wifi", "pool", "spa", "gym", "restaurant", "bar", "business_center", "conference_room", "laundry"],
                ["wifi", "spa", "gym", "restaurant", "bar", "room_service", "concierge", "tennis_court", "golf_course"],
                ["wifi", "pool", "spa", "restaurant", "bar", "room_service", "valet_parking", "shuttle_service", "laundry"]
            ],
            "resort": [
                ["wifi", "pool", "spa", "gym", "restaurant", "bar", "beach_access", "kids_club", "tennis_court"],
                ["wifi", "pool", "spa", "restaurant", "bar", "golf_course", "beach_access", "shuttle_service", "laundry"],
                ["wifi", "pool", "gym", "restaurant", "bar", "kids_club", "tennis_court", "room_service", "concierge"],
                ["wifi", "spa", "restaurant", "bar", "beach_access", "golf_course", "shuttle_service", "valet_parking"]
            ],
            "boutique": [
                ["wifi", "restaurant", "bar", "gym", "spa", "concierge", "laundry"],
                ["wifi", "restaurant", "bar", "room_service", "business_center", "parking"],
                ["wifi", "gym", "restaurant", "bar", "spa", "shuttle_service", "pet_friendly"],
                ["wifi", "restaurant", "bar", "concierge", "laundry", "valet_parking"]
            ],
            "mid_range": [
                ["wifi", "parking", "restaurant", "gym", "business_center", "laundry"],
                ["wifi", "pool", "restaurant", "bar", "parking", "room_service"],
                ["wifi", "gym", "restaurant", "parking", "shuttle_service", "laundry"],
                ["wifi", "restaurant", "bar", "business_center", "parking", "conference_room"]
            ],
            "budget": [
                ["wifi", "parking", "restaurant", "laundry"],
                ["wifi", "parking", "breakfast", "shuttle_service"],
                ["wifi", "restaurant", "parking", "business_center"],
                ["wifi", "parking", "laundry", "pet_friendly"]
            ]
        }

        room_types = ["single", "double", "twin", "suite", "family", "deluxe"]

        room_amenities_by_type = {
            "single": [
                ["ac", "tv", "wifi", "work_desk", "coffee_maker"],
                ["ac", "tv", "wifi", "safe", "hair_dryer"],
                ["ac", "tv", "wifi", "minibar", "iron"],
                ["ac", "tv", "wifi", "work_desk", "shower"]
            ],
            "double": [
                ["ac", "tv", "wifi", "minibar", "safe", "hair_dryer"],
                ["ac", "tv", "wifi", "work_desk", "coffee_maker", "iron"],
                ["ac", "tv", "wifi", "minibar", "balcony", "bathtub"],
                ["ac", "tv", "wifi", "safe", "room_service", "shower"]
            ],
            "twin": [
                ["ac", "tv", "wifi", "work_desk", "coffee_maker", "safe"],
                ["ac", "tv", "wifi", "minibar", "iron", "hair_dryer"],
                ["ac", "tv", "wifi", "balcony", "shower", "safe"],
                ["ac", "tv", "wifi", "work_desk", "room_service", "bathtub"]
            ],
            "suite": [
                ["ac", "tv", "wifi", "minibar", "balcony", "jacuzzi", "safe", "room_service"],
                ["ac", "tv", "wifi", "kitchenette", "balcony", "bathtub", "work_desk", "coffee_maker"],
                ["ac", "tv", "wifi", "minibar", "jacuzzi", "safe", "iron", "hair_dryer"],
                ["ac", "tv", "wifi", "kitchenette", "balcony", "room_service", "work_desk", "bathtub"]
            ],
                        "deluxe": [
                ["ac", "tv", "wifi", "minibar", "balcony", "safe", "bathtub", "hair_dryer"],
                ["ac", "tv", "wifi", "minibar", "jacuzzi", "room_service", "work_desk", "coffee_maker"],
                ["ac", "tv", "wifi", "balcony", "safe", "bathtub", "iron", "hair_dryer"],
                ["ac", "tv", "wifi", "minibar", "jacuzzi", "room_service", "safe", "bathtub"]
            ],
            "family": [
                ["ac", "tv", "wifi", "kitchenette", "safe", "iron", "hair_dryer", "bathtub"],
                ["ac", "tv", "wifi", "minibar", "balcony", "safe", "room_service", "shower"],
                ["ac", "tv", "wifi", "kitchenette", "work_desk", "coffee_maker", "iron", "bathtub"],
                ["ac", "tv", "wifi", "minibar", "safe", "hair_dryer", "room_service", "shower"]
            ]
        }

        hotels_created = 0
        rooms_created = 0

        for i in range(num_hotels):
            city = random.choice(cities)
            area = random.choice(areas_by_city[city])
            hotel_type = random.choice(hotel_types)
            
            prefix = random.choice(hotel_name_prefixes)
            suffix = random.choice(hotel_name_suffixes)
            hotel_name = f"{prefix} {suffix} {area}"
            
            counter = 1
            original_name = hotel_name
            while Hotel.objects.filter(name=hotel_name).exists():
                hotel_name = f"{original_name} {counter}"
                counter += 1

            star_rating_map = {
                "budget": random.choice([2, 3]),
                "mid_range": random.choice([3, 4]),
                "luxury": random.choice([4, 5]),
                "resort": random.choice([4, 5]),
                "boutique": random.choice([3, 4, 5])
            }

            star_rating = star_rating_map[hotel_type]
            amenities = random.choice(amenities_by_type[hotel_type])

            city_coordinates = {
                "Mumbai": (19.0760, 72.8777),
                "Delhi": (28.7041, 77.1025),
                "Bangalore": (12.9716, 77.5946),
                "Chennai": (13.0827, 80.2707),
                "Kolkata": (22.5726, 88.3639),
                "Hyderabad": (17.3850, 78.4867),
                "Pune": (18.5204, 73.8567),
                "Ahmedabad": (23.0225, 72.5714),
                "Jaipur": (26.9124, 75.7873),
                "Goa": (15.2993, 74.1240),
                "Kochi": (9.9312, 76.2673),
                "Coimbatore": (11.0168, 76.9558),
                "Mysore": (12.2958, 76.6394),
                "Udaipur": (24.5854, 73.7125),
                "Agra": (27.1767, 78.0081),
                "Varanasi": (25.3176, 82.9739),
                "Rishikesh": (30.0869, 78.2676),
                "Manali": (32.2396, 77.1887),
                "Shimla": (31.1048, 77.1734),
                "Darjeeling": (27.0360, 88.2627)
            }

            base_lat, base_lng = city_coordinates.get(city, (28.7041, 77.1025))
            # Add small random offset for area variation
            latitude = base_lat + random.uniform(-0.05, 0.05)
            longitude = base_lng + random.uniform(-0.05, 0.05)

            hotel = Hotel.objects.create(
                name=hotel_name,
                description=self.get_hotel_description(hotel_type, city, area, amenities),
                hotel_type=hotel_type,
                city=city,
                area=area,
                address=f"{random.randint(1, 999)} {area} Road, {area}, {city}, India",
                latitude=Decimal(str(round(latitude, 6))),
                longitude=Decimal(str(round(longitude, 6))),
                amenities=amenities,
                star_rating=star_rating,
                average_rating=random.randint(0, star_rating),
                images=self.get_images(random.randint(3, 6)),
                contact_phone=f"+91-{random.randint(7000000000, 9999999999)}",
                contact_email=f"info@{hotel_name.lower().replace(' ', '').replace(',', '')}.com"
            )

            hotels_created += 1

            # Create 3-8 rooms per hotel
            for j in range(random.randint(3, 8)):
                room_type = random.choice(room_types)

                # Set capacity based on room type
                capacity_map = {
                    "single": 1,
                    "double": 2,
                    "twin": 2,
                    "suite": 4,
                    "deluxe": 2,
                    "family": 6
                }

                # Set size based on room type
                size_map = {
                    "single": random.randint(200, 300),
                    "double": random.randint(300, 450),
                    "twin": random.randint(350, 500),
                    "suite": random.randint(600, 1000),
                    "deluxe": random.randint(400, 600),
                    "family": random.randint(500, 800)
                }

                # Set price range based on hotel star rating and room type
                base_price = star_rating * 1000

                price_multiplier = {
                    "single": 0.7,
                    "double": 1.0,
                    "twin": 1.0,
                    "suite": 2.5,
                    "deluxe": 1.8,
                    "family": 2.0
                }

                # Adjust price based on hotel type
                type_multiplier = {
                    "budget": 0.6,
                    "mid_range": 1.0,
                    "luxury": 2.0,
                    "resort": 1.8,
                    "boutique": 1.5
                }

                price = base_price * price_multiplier[room_type] * type_multiplier[hotel_type]
                price += random.randint(-500, 1000)
                price = max(price, 800)

                room_number = f"{j+1:03d}"
                room_amenities = random.choice(room_amenities_by_type[room_type])
                size_sqft = size_map[room_type]
                Room.objects.create(
                    hotel=hotel,
                    room_type=room_type,
                    room_number=room_number,
                    capacity=capacity_map[room_type],
                    price_per_night=Decimal(str(round(price, 2))),
                    amenities=room_amenities,
                    description=self.get_room_description(room_type, room_amenities, size_sqft),
                    size_sqft=size_sqft,
                    images=self.get_images(random.randint(2, 4)),
                )
                rooms_created += 1

        self.stdout.write(f"Hotels created: {hotels_created}")
        self.stdout.write(f"Rooms created: {rooms_created}")
        self.stdout.write(self.style.SUCCESS(f"Successfully generated {hotels_created} hotels with {rooms_created} rooms using hotel-related images!"))
