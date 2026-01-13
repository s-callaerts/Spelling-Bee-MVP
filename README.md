# Spelling Bee MVP

本プロジェクトは、未経験からWebアプリケーション開発を学ぶために個人で開発している学習用プロジェクトです。  
単に動くものを作るだけでなく、設計・セキュリティ・保守性を意識した開発を目標としています。  
将来的には実際にテスト運用を行い、日本の英語教育に貢献できるサービスへ発展させることを目標としています。

また、フロントエンドは現状HTML/CSS/JavaScriptで開発していますが、将来的には **Flutterを使用したクロスプラットフォーム対応** を予定しており、WebだけでなくiOS・Androidアプリとしても利用できる設計を目指しています。

---

## 目的

本アプリは、小学生・中学生を対象に、英単語のスペル学習を支援することを目的としています。

- 生徒は英単語のスペルを学習し、テスト形式で実力を確認可能  
- 学習を競争形式にすることで、読解力や記述力の向上を目指す

### 教師向け管理機能（想定）
- 授業グループの作成と管理  
- 年度ごとの生徒リセットおよび新規招待  
- 教科書の章ごとに対応した練習やテストの配信  
- クラス全体のスコア一覧の確認  
  - 生徒は自分のスコアのみ確認可能  
  - 教師は授業内の全生徒の成績を把握可能

将来的には、校内や地域単位でのランキング機能も検討中で、  
生徒同士が健全に競争しながら成長できる環境を提供することを目指しています。

> ※スコアによる他者への誹謗中傷やいじめ行為は禁止しています。

---

## 使用技術・スキルマップ

| 項目 | スキル・実装内容 | 備考 |

**バックエンド** | Flask, Python | API設計・ルーティング・認証 | User, TestAttempt, Classroomモデル設計、DBアクセス 
**データベース** | SQLite3 / PostgreSQL想定 |テーブル設計・CRUD処理 | ユーザー、スコア、テスト履歴、クラス情報管理 
**セキュリティ** | パスワード暗号化, Sessionチェック, 権限管理 | 教師/生徒ロールのアクセス制御 
**フロントエンド** | HTML, CSS, JavaScript | ダッシュボード, テスト画面, 登録画面 
**Flutter（予定）** | Dart, Flutter | クロスプラットフォーム対応 (Web/iOS/Android) 
**その他** | 非同期JS | フロントとバックのデータ同期、UX改善 

認証・認可ロジックはすべて auth ブループリントに集中させており、各機能ブループリント（テスト、クラスルームなど）はビジネスロジックのみに専念しています。この分離により、保守性が高く、スケーラブルな API 設計を実現しています。

---

## プロジェクトで得た知見

- Flaskを用いたWebアプリケーション設計  
- Pythonによるパスワード暗号化とセキュリティ対策  
- ユーザー、TestAttempt、Classroomモデルの設計と実装  
- Schemaによるバリデーション・セッションチェック・権限管理の実装  
- 環境変数やアクセス権限を用いた機密情報管理  
- データベース設計及び接続処理（SQLite3 / PostgreSQL想定）  
- フロントエンドとバックエンドの連携  
- 非同期JavaScriptの基礎と実装経験  

---

## 現在できること

- Flask + SQLによるAPI設計とデータ操作  
- ユーザー認証・権限管理・テストスコア管理  
- フロントエンド（HTML/JS）でのAPI呼び出し・非同期表示  
- DBモデル・Schemaを用いた堅牢なデータ管理  

---

## 今後の学習予定

- Flutterフロントエンドの習得・実装  
- UI/UX改善  
- 認証や権限管理の強化  
- テストコードの追加  
- 本番環境を想定したデプロイ経験  

---

本プロジェクトは、**フルスタック開発スキルを学ぶ過程そのもの**を記録したものです。  
今後も改善を続け、より堅牢で魅力的なアプリケーションに成長させていきます。


# Spelling Bee MVP

This project is a personal learning project developed to study web application development from scratch.  
Rather than simply creating a working application, the focus is on **software design, security, and maintainability**.

The long-term goal is to run real test deployments and eventually evolve this project into a service that can contribute to English education in Japan.

Currently, the frontend is implemented using HTML/CSS/JavaScript for development and testing purposes.  
In the future, the frontend is planned to be rebuilt using **Flutter**, enabling cross-platform support for Web, iOS, and Android applications.

---

## Purpose

This application is designed to support English spelling learning for elementary and junior high school students.

- Students can practice English spelling and assess their skills through test-based exercises  
- A competitive learning format is used to encourage motivation and improve writing and comprehension skills  

### Planned Teacher Features
- Creation and management of classroom groups  
- Yearly student reset and new student invitations  
- Distribution of practice exercises and tests aligned with textbook chapters  
- Viewing class-wide score summaries  
  - Students can only view their own scores  
  - Teachers can view all student results within their classroom  

In the future, the application may expand beyond individual classes to include **school-wide or regional rankings**, promoting healthy competition and continuous improvement among students.

> ※ Any misuse of score data, including harassment or bullying, is strictly prohibited.

---

## Technology Stack & Skill Map

| Category | Technologies | Description | Details |

**Backend** | Flask, Python | API design, routing, authentication | User, TestAttempt, Classroom model design and DB access 
**Database** | SQLite3 / PostgreSQL (planned) | Table design and CRUD operations | User data, test history, scores, classroom relationships 
**Security** | Password hashing, session checks, role-based access control | Teacher / Student permission enforcement 
**Frontend** | HTML, CSS, JavaScript | Dashboard, test screens, registration pages 
**Flutter (planned)** | Dart, Flutter | Cross-platform frontend (Web / iOS / Android) 
**Other** | Async JavaScript, REST API integration | Frontend-backend data synchronization, UX improvements 

All authentication and authorization logic is centralized in the auth blueprint, while feature blueprints focus on business logic. This separation ensures secure, maintainable, and scalable API design.

---

## Knowledge & Experience Gained

- Web application architecture using Flask  
- Password hashing and backend-focused security practices in Python  
- Design and implementation of User, TestAttempt, and Classroom domain models  
- Server-side validation, session checks, and role-based authorization  
- Database schema design and connection handling (SQLite3 / PostgreSQL planned)  
- Frontend and backend integration via REST APIs  
- Asynchronous JavaScript implementation for improved user experience  

---

## Current Capabilities

- Designing RESTful APIs using Flask and Python  
- Implementing user authentication and role-based access control  
- Managing test attempts, scores, and classroom data  
- Designing database schemas and performing CRUD operations  
- Connecting frontend applications to backend APIs using asynchronous requests  

---

## Future Work & Learning Goals

- Implementing a Flutter-based frontend  
- UI / UX improvements  
- Enhancing authentication and authorization mechanisms  
- Adding automated tests  
- Gaining deployment experience for production environments  

---

This project represents **my growth process as a full-stack developer**.  
Development will continue with a focus on clean architecture, security, and scalability