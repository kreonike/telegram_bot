from deepface import DeepFace
import json
from pprint import pprint

def face_analyze():
    try:
        result_dict = DeepFace.analyze(img_path='4.jpg', actions=['age', 'gender', 'race', 'emotion'])

        with open('face_analyze.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)


        print(f'[+] Age: {result_dict.get("age")}')
        print(f'[+] Gender: {result_dict.get("gender")}')
        race = result_dict.get("race")
        max_val_race = max(race.values())
        final_dict_race = {k: v for k, v in race.items() if v == max_val_race}
        keys = list(final_dict_race .keys())
        print(f'[+] Race: {keys[0]}')

        emotion = result_dict.get("emotion")
        max_val_emo = max(emotion.values())
        final_dict_emo = {k: v for k, v in emotion.items() if v == max_val_emo}
        keys = list(final_dict_emo.keys())
        print(f'[+] Emotions: {keys[0]}')



        # print('[+] Emotions:')
        #
        # for k, v in result_dict.get('emotion').items():
        #     print(f'{k} - {round(v, 2)}%')



        return result_dict

    except Exception as _ex:
        return _ex


def main():
    face_analyze()



if __name__ == '__main__':
    main()