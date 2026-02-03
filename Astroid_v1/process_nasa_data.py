import json

# Load NASA JPL data
with open('nasa_sbdb_full.json', 'r') as f:
    asteroid_data = json.load(f)

# Load comet data if exists
try:
    with open('nasa_sbdb_comets.json', 'r') as f:
        comet_data = json.load(f)
except:
    comet_data = {'fields': [], 'data': []}

# Orbit class mapping
orbit_classes_map = {
    'MBA': 16,  # Main-belt Asteroid
    'OMB': 18,  # Outer Main-belt
    'IMB': 15,  # Inner Main-belt
    'AMO': 8,   # Amor
    'APO': 9,   # Apollo
    'ATE': 11,  # Aten
    'MCA': 17,  # Mars-crosser
    'TJN': 20,  # Jupiter Trojan
    'CEN': 12,  # Centaur
    'TNO': 21,  # Trans-Neptunian
    'AST': 10,  # Asteroid (unclassified)
    'COM': 1,   # Unclassified Comet
    'CTc': 2,   # Chiron-type Comet
    'ETc': 3,   # Encke-type Comet
    'HTC': 4,   # Halley-type Comet
    'HYP': 5,   # Hyperbolic Comet
    'JFc': 6,   # Jupiter-family Comet
    'PAR': 7,   # Parabolic Comet
}

# Orbit class definitions
orbit_classes = [
    {"id": 1, "name": "Unclassified Comet", "slug": "unclassified-comets", "abbrev": "COM", "desc": "Comets whose orbits do not match any defined orbit class", "orbit_sentence": "whose orbit does not match any defined comet orbit class"},
    {"id": 2, "name": "Chiron-type Comet", "slug": "chiron-type-comets", "abbrev": "CTc", "desc": "Chiron-type comet, as defined by Levison and Duncan (TJupiter > 3; a > aJupiter)", "orbit_sentence": "whose orbit is approximately between Jupiter and Neptune"},
    {"id": 3, "name": "Encke-type Comet", "slug": "encke-type-comets", "abbrev": "ETc", "desc": "Encke-type comet, as defined by Levison and Duncan (TJupiter > 3; a < aJupiter)", "orbit_sentence": "whose orbit brings it closer to the sun than Jupiter"},
    {"id": 4, "name": "Halley-type Comet", "slug": "halley-type-comets", "abbrev": "HTC", "desc": "Halley-type comet, classical definition (20 y < P < 200 y)", "orbit_sentence": "with a medium-length orbit that is highly inclined to the ecliptic plane of the solar system"},
    {"id": 5, "name": "Hyperbolic Comet", "slug": "hyperbolic-comets", "abbrev": "HYP", "desc": "Comets on hyperbolic orbits (e > 1.0)", "orbit_sentence": "with a trajectory through the solar system likely originating from the Oort Cloud"},
    {"id": 6, "name": "Jupiter-family Comet", "slug": "jupiter-family-comets", "abbrev": "JFc", "desc": "Jupiter-family comets, as defined by Levison and Duncan (2 < TJupiter < 3)", "orbit_sentence": "whose orbit features a relatively short period, low inclination, and is controlled by Jupiter's gravitational effects"},
    {"id": 7, "name": "Parabolic Comet", "slug": "parabolic-comets", "abbrev": "PAR", "desc": "Comets on parabolic orbits (e = 1.0)", "orbit_sentence": "with a marginal orbit that brings it from the outer reaches of the solar system"},
    {"id": 8, "name": "Amor-class Asteroid", "slug": "amor", "abbrev": "AMO", "desc": "Near-Earth asteroid whose orbits are similar to that of 1221 Amor (a > 1.0 AU; 1.017 AU < q < 1.3 AU)", "orbit_sentence": "with a perihelion distance between 1.017 and 1.3 AU"},
    {"id": 9, "name": "Apollo-class Asteroid", "slug": "apollo", "abbrev": "APO", "desc": "Near-Earth asteroids whose orbits cross the Earth's orbit similar to that of 1862 Apollo (a > 1.0 AU; q < 1.017 AU).", "orbit_sentence": "that is a Near-Earth Asteroid and periodically crosses Earth's orbit"},
    {"id": 10, "name": "Asteroid", "slug": "asteroid", "abbrev": "AST", "desc": "Asteroid orbit not matching any defined orbit class", "orbit_sentence": "that does not match any defined orbit class"},
    {"id": 11, "name": "Aten-class Asteroid", "slug": "aten", "abbrev": "ATE", "desc": "Near-Earth asteroid orbits similar to that of 2062 Aten (a < 1.0 AU; Q > 0.983 AU)", "orbit_sentence": "that has a semimajor axis of less than one AU"},
    {"id": 12, "name": "Centaur-class Asteroid", "slug": "centaur", "abbrev": "CEN", "desc": "Objects with orbits between Jupiter and Neptune (5.5 AU < a < 30.1 AU)", "orbit_sentence": "with an orbit between Jupiter and Neptune"},
    {"id": 13, "name": "Hyperbolic Asteroid", "slug": "hyperbolic", "abbrev": "HYP", "desc": "Asteroids on hyperbolic orbits (e > 1.0)", "orbit_sentence": "with a strongly hyperbolic trajectory"},
    {"id": 14, "name": "Interior-Earth Asteroid", "slug": "ies", "abbrev": "IEO", "desc": "Asteroids with orbits contained entirely within the orbit of the Earth (Q < 0.983 AU)", "orbit_sentence": "that orbits entirely within Earth's orbit"},
    {"id": 15, "name": "Inner Main-belt Asteroid", "slug": "imb", "abbrev": "IMB", "desc": "Asteroids with orbital elements constrained by (a < 2.0 AU; q > 1.666 AU)", "orbit_sentence": "that is in the inner part of the asteroid belt"},
    {"id": 16, "name": "Main-belt Asteroid", "slug": "mba", "abbrev": "MBA", "desc": "Asteroids with orbital elements constrained by (2.0 AU < a < 3.2 AU; q > 1.666 AU)", "orbit_sentence": "that is in the main asteroid belt between Mars and Jupiter"},
    {"id": 17, "name": "Mars-crossing Asteroid", "slug": "mars-crosser", "abbrev": "MCA", "desc": "Asteroids that cross the orbit of Mars constrained by (1.3 AU < q < 1.666 AU; a < 3.2 AU)", "orbit_sentence": "that crosses the orbit of Mars"},
    {"id": 18, "name": "Outer Main-belt Asteroid", "slug": "omb", "abbrev": "OMB", "desc": "Asteroids with orbital elements constrained by (3.2 AU < a < 4.6 AU)", "orbit_sentence": "that is in the outer part of the asteroid belt"},
    {"id": 19, "name": "Parabolic Asteroid", "slug": "parabolic", "abbrev": "PAR", "desc": "Asteroids on parabolic orbits (e = 1.0)", "orbit_sentence": "on a parabolic trajectory"},
    {"id": 20, "name": "Jupiter Trojan", "slug": "trojan", "abbrev": "TJN", "desc": "Asteroids trapped in Jupiter's L4/L5 Lagrange points (4.6 AU < a < 5.5 AU; e < 0.3)", "orbit_sentence": "that is a Trojan asteroid near one of Jupiter's Lagrange points"},
    {"id": 21, "name": "Trans-Neptunian Object", "slug": "tno", "abbrev": "TNO", "desc": "Objects with orbits outside Neptune (a > 30.1 AU)", "orbit_sentence": "with an orbit beyond Neptune"}
]

# Create orbit class lookup
orbit_class_lookup = {oc['id']: oc for oc in orbit_classes}

# Process asteroids
objects = []
fields = asteroid_data['fields']

print(f"Processing {len(asteroid_data['data'])} asteroids...")
for row in asteroid_data['data']:
    obj = dict(zip(fields, row))
    
    # Get orbit class info
    class_abbrev = obj['class']
    orbit_class_id = orbit_classes_map.get(class_abbrev, 10)
    orbit_class_info = orbit_class_lookup[orbit_class_id]
    
    # Create object
    objects.append({
        'slug': obj['pdes'].lower().replace(' ', '-').replace('(', '').replace(')', ''),
        'fullname': obj['full_name'],
        'name': obj['name'] if obj['name'] else obj['pdes'],
        'a': float(obj['a']),
        'e': float(obj['e']),
        'i': float(obj['i']),
        'ma': float(obj['ma']),
        'om': float(obj['om']),
        'w': float(obj['w']),
        'H': float(obj['H']) if obj['H'] else None,
        'diameter': float(obj['diameter']) if obj['diameter'] else None,
        'diameter_estimate': None,
        'spec_B': obj['spec_B'],
        'spec_T': obj['spec_T'],
        'is_pha': obj['pha'] == 'Y',
        'is_nea': obj['neo'] == 'Y',
        'object_type': 'asteroid',
        'orbit_class_id': orbit_class_id,
        'orbit_class': orbit_class_info
    })

# Process comets if available
if comet_data['data']:
    print(f"Processing {len(comet_data['data'])} comets...")
    fields = comet_data['fields']
    for row in comet_data['data']:
        obj = dict(zip(fields, row))
        
        class_abbrev = obj.get('class', 'COM')
        orbit_class_id = orbit_classes_map.get(class_abbrev, 1)
        orbit_class_info = orbit_class_lookup[orbit_class_id]
        
        objects.append({
            'slug': obj['pdes'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-'),
            'fullname': obj['full_name'],
            'name': obj.get('name') if obj.get('name') else obj['pdes'],
            'a': float(obj['a']) if obj.get('a') else None,
            'e': float(obj['e']) if obj.get('e') else None,
            'i': float(obj['i']) if obj.get('i') else None,
            'ma': float(obj['ma']) if obj.get('ma') else None,
            'om': float(obj['om']) if obj.get('om') else None,
            'w': float(obj['w']) if obj.get('w') else None,
            'H': float(obj['H']) if obj.get('H') else None,
            'diameter': float(obj['diameter']) if obj.get('diameter') else None,
            'diameter_estimate': None,
            'spec_B': obj.get('spec_B'),
            'spec_T': obj.get('spec_T'),
            'is_pha': obj.get('pha') == 'Y',
            'is_nea': obj.get('neo') == 'Y',
            'object_type': 'comet',
            'orbit_class_id': orbit_class_id,
            'orbit_class': orbit_class_info
        })

# Create final output
output = {
    'orbit_classes': orbit_classes,
    'objects': objects
}

# Save to file
with open('comprehensive_nasa_data.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✅ SUCCESS!")
print(f"📊 Total objects: {len(objects)}")
print(f"🌑 Asteroids: {len([o for o in objects if o['object_type'] == 'asteroid'])}")
print(f"☄️  Comets: {len([o for o in objects if o['object_type'] == 'comet'])}")
print(f"📁 Saved to: comprehensive_nasa_data.json")





