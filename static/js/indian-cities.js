const INDIAN_CITIES = [
    // Major Metropolitan Cities
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
    'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat',
    
    // Tier 1 Cities
    'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane',
    'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara',
    'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad',
    'Meerut', 'Rajkot', 'Kalyan-Dombivli', 'Vasai-Virar', 'Varanasi',
    
    // Tier 2 Cities
    'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Navi Mumbai',
    'Allahabad', 'Ranchi', 'Howrah', 'Coimbatore', 'Jabalpur',
    'Gwalior', 'Vijayawada', 'Jodhpur', 'Madurai', 'Raipur',
    'Kota', 'Chandigarh', 'Guwahati', 'Solapur', 'Hubli-Dharwad',
    
    // State Capitals and Important Cities
    'Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Kollam',
    'Mysore', 'Mangalore', 'Belgaum', 'Gulbarga', 'Davangere',
    'Tirupati', 'Guntur', 'Nellore', 'Kurnool', 'Rajahmundry',
    'Warangal', 'Nizamabad', 'Khammam', 'Karimnagar', 'Mahbubnagar',
    
    // Tamil Nadu Cities
    'Salem', 'Tiruchirappalli', 'Tirunelveli', 'Erode', 'Vellore',
    'Thoothukudi', 'Dindigul', 'Thanjavur', 'Cuddalore', 'Kanchipuram',
    
    // Karnataka Cities
    'Shimoga', 'Tumkur', 'Bijapur', 'Hospet', 'Gadag-Betageri',
    'Udupi', 'Bidar', 'Robertson Pet', 'Bhadravati', 'Chitradurga',
    
    // Andhra Pradesh & Telangana
    'Kadapa', 'Anantapur', 'Chittoor', 'Eluru', 'Machilipatnam',
    'Adilabad', 'Suryapet', 'Miryalaguda', 'Jagtial', 'Mancherial',
    
    // Maharashtra Cities
    'Kolhapur', 'Sangli', 'Jalgaon', 'Akola', 'Latur',
    'Dhule', 'Ahmednagar', 'Chandrapur', 'Parbhani', 'Ichalkaranji',
    'Jalna', 'Ambajogai', 'Bhusawal', 'Panvel', 'Badlapur',
    'Beed', 'Gondia', 'Satara', 'Barshi', 'Yavatmal',
    
    // Gujarat Cities
    'Bhavnagar', 'Jamnagar', 'Junagadh', 'Gandhinagar', 'Nadiad',
    'Morbi', 'Mahesana', 'Bharuch', 'Vapi', 'Navsari',
    'Veraval', 'Porbandar', 'Godhra', 'Bhuj', 'Anand',
    
    // Rajasthan Cities
    'Udaipur', 'Ajmer', 'Bikaner', 'Alwar', 'Bharatpur',
    'Pali', 'Barmer', 'Sikar', 'Tonk', 'Kishangarh',
    'Beawar', 'Hanumangarh', 'Sri Ganganagar', 'Jhunjhunu', 'Churu',
    
    // Uttar Pradesh Cities
    'Ghaziabad', 'Noida', 'Greater Noida', 'Moradabad', 'Aligarh',
    'Saharanpur', 'Bareilly', 'Gorakhpur', 'Firozabad', 'Muzaffarnagar',
    'Mathura', 'Rampur', 'Shahjahanpur', 'Farrukhabad', 'Mau',
    'Hapur', 'Etawah', 'Mirzapur', 'Bulandshahr', 'Sambhal',
    'Amroha', 'Hardoi', 'Fatehpur', 'Raebareli', 'Orai',
    'Sitapur', 'Bahraich', 'Modinagar', 'Unnao', 'Jhansi',
    'Lakhimpur', 'Hathras', 'Banda', 'Pilibhit', 'Barabanki',
    'Khurja', 'Gonda', 'Mainpuri', 'Lalitpur', 'Etah',
    
    // Madhya Pradesh Cities
    'Ujjain', 'Dewas', 'Satna', 'Ratlam', 'Rewa',
    'Sagar', 'Singrauli', 'Burhanpur', 'Khandwa', 'Bhind',
    'Chhindwara', 'Guna', 'Shivpuri', 'Vidisha', 'Chhatarpur',
    'Damoh', 'Mandsaur', 'Khargone', 'Neemuch', 'Pithampur',
    
    // West Bengal Cities
    'Durgapur', 'Asansol', 'Siliguri', 'Bardhaman', 'Malda',
    'Baharampur', 'Habra', 'Kharagpur', 'Shantipur', 'Dankuni',
    'Dhulian', 'Ranaghat', 'Haldia', 'Raiganj', 'Krishnanagar',
    'Nabadwip', 'Medinipur', 'Jalpaiguri', 'Balurghat', 'Basirhat',
    
    // Bihar Cities
    'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Purnia', 'Darbhanga',
    'Bihar Sharif', 'Arrah', 'Begusarai', 'Katihar', 'Munger',
    'Chhapra', 'Danapur', 'Saharsa', 'Sasaram', 'Hajipur',
    'Dehri', 'Siwan', 'Motihari', 'Nawada', 'Bagaha',
    
    // Jharkhand Cities
    'Jamshedpur', 'Bokaro', 'Deoghar', 'Phusro', 'Hazaribagh',
    'Giridih', 'Ramgarh', 'Medininagar', 'Chirkunda', 'Pakaur',
    
    // Odisha Cities
    'Bhubaneswar', 'Cuttack', 'Rourkela', 'Brahmapur', 'Sambalpur',
    'Puri', 'Balasore', 'Bhadrak', 'Baripada', 'Jharsuguda',
    
    // Punjab Cities
    'Jalandhar', 'Patiala', 'Bathinda', 'Hoshiarpur', 'Batala',
    'Pathankot', 'Moga', 'Abohar', 'Malerkotla', 'Khanna',
    'Phagwara', 'Muktsar', 'Barnala', 'Rajpura', 'Firozpur',
    
    // Haryana Cities
    'Gurugram', 'Panipat', 'Ambala', 'Yamunanagar', 'Rohtak',
    'Hisar', 'Karnal', 'Sonipat', 'Panchkula', 'Bhiwani',
    'Sirsa', 'Bahadurgarh', 'Jind', 'Thanesar', 'Kaithal',
    'Palwal', 'Rewari', 'Hansi', 'Narnaul', 'Fatehabad',
    
    // Himachal Pradesh Cities
    'Shimla', 'Solan', 'Dharamshala', 'Mandi', 'Palampur',
    'Baddi', 'Nahan', 'Paonta Sahib', 'Sundarnagar', 'Chamba',
    
    // Uttarakhand Cities
    'Dehradun', 'Haridwar', 'Roorkee', 'Haldwani-cum-Kathgodam', 'Rudrapur',
    'Kashipur', 'Rishikesh', 'Ramnagar', 'Pithoragarh', 'Jaspur',
    
    // Jammu & Kashmir Cities
    'Jammu', 'Baramula', 'Anantnag', 'Sopore', 'KathUA',
    'Rajauri', 'Punch', 'Udhampur', 'Kathua', 'Samba',
    
    // Assam Cities
    'Dibrugarh', 'Silchar', 'Tezpur', 'Nagaon', 'Tinsukia',
    'Jorhat', 'Bongaigaon', 'Dhubri', 'Diphu', 'North Lakhimpur',
    
    // Kerala Cities
    'Kannur', 'Kasaragod', 'Kottayam', 'Alappuzha', 'Palakkad',
    'Malappuram', 'Thrissur', 'Idukki', 'Wayanad', 'Pathanamthitta',
    
    // Other State Cities
    'Agartala', 'Aizawl', 'Imphal', 'Kohima', 'Itanagar',
    'Gangtok', 'Shillong', 'Dispur', 'Panaji', 'Silvassa',
    'Daman', 'Kavaratti', 'Port Blair', 'Puducherry'
];

// Function to get all cities
function getIndianCities() {
    return INDIAN_CITIES.sort();
}

// Function to search cities
function searchIndianCities(query) {
    if (!query || query.length < 2) {
        return [];
    }
    
    const searchTerm = query.toLowerCase();
    return INDIAN_CITIES.filter(city => 
        city.toLowerCase().includes(searchTerm)
    ).sort();
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { INDIAN_CITIES, getIndianCities, searchIndianCities };
}
