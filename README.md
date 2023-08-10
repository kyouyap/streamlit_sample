## AIチャットアプリリポジトリ

このリポジトリでは、AIチャットアプリケーションの構築に必要なスクリプトとツールが提供されています。このアプリケーションはユーザーからのメッセージに対応するAIの回答を生成し、ユーザーとの対話をサポートします。

## ファイル構成

- `00_streaming_chat.py`: 基本的なストリーミングチャットの実装。
- `01_base_chat.py`: ベースとなるチャットの実装。
- `02_ai_chat.py`: AIを使ったチャットの実装。
- `03_summary.py`: チャットの要約を生成するスクリプト。
- `04_youtube_summary.py`: YouTubeのビデオの要約を生成するスクリプト。
- `05_youtube_summary_added.py`: YouTubeのビデオ要約の機能を追加したチャットのスクリプト。
- `06_PDF_chat.py`: PDFをアップロードしてその要約を生成するチャットのスクリプト。
- `07_codeinterpreter.py`: ユーザーからのコードスニペットを解釈するためのスクリプト。
- `Pipfile`: プロジェクトに必要なPythonパッケージのリスト。
- `Pipfile.lock`: pipenvが生成する、プロジェクトの依存関係についての詳細な情報を含むファイル。
- `code_interpreter.py`: ユーザーからのコードスニペットを解釈し、適切なレスポンスを生成するためのモジュール。
- `db_manager.py`: データベース操作を担当するモジュール。
- `token_cost_process.py`: トークンのコストを処理するスクリプト。
- `.env_sample`:環境変数を管理するファイル。

## セットアップ

このプロジェクトではpipenv,devcontainerを使って依存関係を管理しています。プロジェクトのセットアップは.envファイルを作成し、devcontainerを作ることで行えます。
streamlitでアプリを動かすには`streamlit run hogehoge.py`で実行してください。


## 注意

このプロジェクトは現在進行中で、一部の機能はまだ完成していません。詳細は各スクリプトのコメントやdocstringをご覧ください。あらゆる提案や改善のためのプルリクエストは大歓迎です。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)をご覧ください。

## 著者
kyouyap

## 貢献

このプロジェクトに貢献したい方は、まずはIssueを作成するか、既存のIssueにコメントしてください。また、Pull Requestも大歓迎です。
