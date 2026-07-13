# הקוד מאפשר למשתמש לחפש ולשלוף באופן דינמי את 10 הנתונים הראשונים של השכבה שנבחרה בטבלה מסודרת ולערוך על הנתונים מוניפולציות

import requests
import pandas as pd

BASE_URL = "https://gisviewer.jerusalem.muni.il/arcgis/rest/services/BaseLayers/MapServer"

# הגדרת כותרת דפדפן כדי שהשרת יזהה אותנו כמשתמש רגיל ולא יחסום את הפנייה (שגיאה 403)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_available_layers():
    """GIS-שליפת רשימת השכבות הזמינות מ"""
    try:
        response = requests.get(BASE_URL, params={'f': 'json'}, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return {layer['name']: layer['id'] for layer in data.get('layers', [])}
    except requests.exceptions.RequestException as e:
        print(f"שגיאה במיפוי השכבות: {e}")
        return None

def fetch_layer_data(layer_id, limit=10):
    """שולפת נתונים עבור שכבה ספציפית לפי המזהה שלה ומחזירה דאטה פריים של פאנדס"""
    url = f"{BASE_URL}/{layer_id}/query"
    # שאילתה חסרת משמעות אמיתית של שליפת 10 הנתונים הראשונים בלי שום סינון
    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'json',
        'resultRecordCount': limit,
        'returnGeometry': 'false'
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        features = response.json().get('features', [])
        if features:
            return pd.DataFrame([feature['attributes'] for feature in features])
        return None
    except requests.exceptions.RequestException as e:
        print(f"שגיאה בשליפת הנתונים: {e}")
        return None

def main():
    print("\n=== ברוכים הבאים למערכת שליפת נתוני GIS ===")
    
    knows_id = input("האם ידוע לך מספר השכבה (ID)? (כן/לא): ").strip()
    
    # אתחול משתנה שיחזיק את מזהה השכבה שנרצה לשלוף בסוף
    layer_id_to_fetch = None
    
    # בדיקה האם המשתמש ענה בחיוב
    if knows_id in ['כן', 'yes', 'y', 'כ', '1']:
        try:
            layer_id_to_fetch = int(input("אנא הכנס את מספר השכבה: ").strip())
        except ValueError:
            print("שגיאה: יש להכניס מספרים בלבד. התוכנית תסתיים.")
            return
            
    else:
        print("מתחבר לשרת לטעינת רשימת השכבות...")
        layers_map = get_available_layers()
        
        if not layers_map:
            print("שגיאה: לא ניתן לטעון את השכבות מהשרת כרגע.")
            return
            
        # קבלת מילת חיפוש מהמשתמש כדי לצמצם את האפשרויות
        keyword = input("הכנס מילת חיפוש (למשל 'חינוך', 'אוטובוס', 'חניה'): ").strip()
        
        matching_layers = {name: id for name, id in layers_map.items() if keyword in name}
        
        if not matching_layers:
            print(f"לא נמצאו שכבות המכילות את המילה '{keyword}'.")
            return
            
        # אם נמצאה רק שכבה אחת בדיוק שתואמת לחיפוש
        elif len(matching_layers) == 1:
            name, id = list(matching_layers.items())[0]
            print(f"נמצאה התאמה יחידה: '{name}' (מזהה: {id}). בוחר אוטומטית...")
            layer_id_to_fetch = id
            
        else:
            # הצגת כמות השכבות שנמצאו
            print(f"נמצאו {len(matching_layers)} שכבות מתאימות:")
            matches_list = list(matching_layers.items())
            
            for index, (name, id) in enumerate(matches_list, 1):
                print(f"[{index}] {name} (מזהה: {id})")
                
            try:
                choice = int(input("הקש את מספר השורה הרצויה מתוך הרשימה: ").strip())
                if 1 <= choice <= len(matches_list):
                    layer_id_to_fetch = matches_list[choice - 1][1]
                    print(f"בחרת ב: '{matches_list[choice - 1][0]}'")
                else:
                    print("בחירה מחוץ לטווח הרשימה. התוכנית תסתיים.")
                    return
            except ValueError:
                print("שגיאה: יש להכניס את המספר הסידורי בלבד.")
                return

    if layer_id_to_fetch is not None:
        print(f"\nמתחיל בשליפת הנתונים עבור שכבה מספר {layer_id_to_fetch}...")
        df = fetch_layer_data(layer_id_to_fetch, limit=10)
        
        if df is not None:
            print("\n=== הנתונים התקבלו בהצלחה! ===")
            print(df)

            # OBJECTID מוניפולציה חסרת משמעות על הנתונים, שמירה רק על עמודת 
            cols_to_keep = ['OBJECTID']
            df = df[cols_to_keep]
            print(df)
        else:
            print("לא חזרו נתונים מהשרת עבור שכבה זו.")

if __name__ == "__main__":
    main()