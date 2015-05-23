cxxtags
=======

**cxxtags** はlibclangを使ってC/C++のソースファイルにタグ付け/インデックシングを行うツールです。ctagsなどのツールとの
大きな違いはC++の文法(例: class, namespace, templateなど)を理解したタグ付けと参照の情報の生成が行えることです。

さまざまIDE(Visual Studio, Eclipse, Xcodeなど) で既にこの機能は実現されていますが、その機能はIDE内部にに組み込まれており
vimなどのエディターから使用することが困難です。**cxxtags** は軽量でポータブルなソースコードタグ付けシステムを目指しています。

必要なライブラリなど
------------------------

* llvm, clang
    * http://llvm.org/
* leveldb
    * https://code.google.com/p/leveldb/
* py-leveldb
    * Thread-safe Python bindings for LevelDB. 
    * https://code.google.com/p/py-leveldb/

**cxxtags**の開発及び動作確認はUbuntu 14.04, python-2.7.6, clang(LLVM)-3.4という環境で行っております。

ビルド方法
------------------------

* 依存ライブラリをインストール
* レポジトリからソースをダウンロード

        $ git clone https://github.com/katonori/cxxtags.git

* ビルド
    * cmakeを実行します。llvm-configがパスに含まれている必要があります。
    * libleveldb.soがコンパイラのデフォルトのサーチパスにない場合は LEVELDB\_HOME でlibleveldb がインストール
      されているディレクトリを指定してください。

            $ mkdir -p build && cd build
            $ cmake -DLEVELDB_HOME=/usr/local ../
            $ make
            $ make install

* インストール
    * ${CXXTAGS\_REPOSITORY\_ROOT}/bin に生成されたファイルをお望みのディレクトリにコピーしてください。

* cygwinでのビルドに関する情報は[README.cygwin.md](README.cygwin.md "")を参照してください。

使い方
------------------------

### タグデータベース作成

タグデータベースを生成するには *cxxtags* コマンドを使用します。

        $ cxxtags _db a.cpp

### データベースに対してクエリ(問い合わせ)を実行

生成したデータベースから情報を得るには *cxxtags_query* コマンドを使用します。
たとえば、a.cppの30行目の8列目で参照されている関数が定義されている箇所の情報を得たい場合、
下記コマンドを実行します。

        $ cxxtags_query def _db a.cpp 30 8

a.cppが下記の内容だった場合

```C
#include <iostream>
namespace NS0 {
    class C0 {
        public:
            void f0() { std::cout << "C0::f0\n"; }
            void f1() { std::cout << "C0::f1\n"; }
    };
    class C1 {
        public:
            void f0() { std::cout << "C1::f0\n"; }
            void f1() { std::cout << "C1::f1\n"; }
    };
};
namespace NS1 {
    class C0 {
        public:
            void f0() { std::cout << "C0::f0\n"; }
            void f1() { std::cout << "C0::f1\n"; }
    };
    class C1 {
        public:
            void f0() { std::cout << "C1::f0\n"; }
            void f1() { std::cout << "C1::f1\n"; }
    };
};

int main()
{
    NS1::C0 c0;
    c0.f1();
    return 0;
}
```

下記のような出力が得られます。

        f1|/home/user0/devel/cxxtags/src/build/a.cpp|18|18|            void f1() { std::cout << "C0::f1\n"; }

vimをお使いの方は *cxxtags_query* のラッパープラグイン[cxxtags-vim](https://github.com/katonori/cxxtags-vim)をご利用ください。

### CMakeLists.txtからのタグデータベース生成

**cxxtags** は正確な情報を得るために、"-I", "-D"などのコンパイルオプションが必要になるため、
実際の利用の際にはCMakeLists.txtから生成されたコンピレーションデータベース(compile\_commands.json)からタグデータベースを生成する
**cxxtags_run_proj**の利用をお勧めします。
**cxxtags_run_proj**の使い方は下記の通りです。

* cmakeにオプション`-DCMAKE_EXPORT_COMPILE_COMMANDS=1`を指定するとビルド対象のファイルやコンパイルオプションなどが
  記録されているcompile\_commands.jsonが生成されます。
* このファイルを入力としてcxxtags\_run\_projを実行します。下記の例では"\_db"にタグデータベースが作成されます。

        $ cxxtags_run_proj _db compile_commands.json

* cmakeではなくMakefileなどを使ったプロジェクトでも[Bear](https://github.com/rizsotto/Bear.git)などのツールを使って
  compile_commands.jsonを生成することができます。
  compile_commands.jsonについての詳細な情報はclangのサイト[http://clang.llvm.org/docs/JSONCompilationDatabase.html](http://clang.llvm.org/docs/JSONCompilationDatabase.html)などを参照してください。 .

コマンド
------------------------

### cxxtags\_run\_proj
cmakeのコンピレーションデータベースからタグデータベースを生成します。
内部でcxxtagsを呼び出しています。

    usage: cxxtags_run_proj [-J] [-j N] [-e exclude_list] database_dir file_name

* -j N
	* Nスレッドで並列にcxxtagsを実行します。
* -J
	* システムのCPU数を自動で検出し、CPU数分のスレッドを生成しcxxtagsを実行します。
* -e
	* タグ付けから除外するディレクトリを指定します。ディレクトリは"/usr/include:/usr/local/include"のように':' で
      区切ることによって複数指定できます。
* database\_dir
    * タグデータベースの出力ディレクトリを指定します。
* file\_name
    * コンピレーションデータベースファイルを指定します。

### cxxtags
指定されたソースコードのデータベースファイルを生成します。

    usage: cxxtags [-e exclude_list] database_dir input_file [-- compiler_arguments]

* -e  
  * タグ付けから除外したいファイルが含まれるディレクトリを指定します。ディレクトリは"/usr/include:/usr/local/include"のように':' で
    区切ることによって複数列挙することが可能です。
* database\_dir
  * タグデータベースの出力ディレクトリを指定します。
* input\_file
  * 入力ファイルを指定します
* compiler\_arguments
  * ファイルをコンパイルするのに必要なオプションを指定します。

### cxxtags\_query
クエリ(問い合わせ)をタグデータベースに対して実行します。

    usage: cxxtags_query query_type[decl/def/ref/override] database_dir file_name line_no column_no

* query\_type: クエリのタイプを指定します。サポートされているクエリの種類は下記の通りです。
    * decl: 指定された箇所にある要素の**宣言** に関するクエリを実行します。
    * def: 指定された箇所にある要素の**定義** に関するクエリを実行します。
    * ref: 指定された箇所にある要素の**参照** に関するクエリを実行します。
    * override: 指定された箇所にある要素の**オーバーライド** に関するクエリを実行します。
* file\_name: クエリを行いたい要素が存在するファイル名を指定します。
* database\_dir: **cxxtags**, **cxxtags_run_proj** によって生成されたデータベースのディレクトリを指定します。
  "db0,db1,db2"のように','で区切って複数のディレクトリを列挙することが可能です。
* line\_no: クエリを行いたい要素が存在する行番号を指定します。
* column\_no: クエリを行いたい要素が存在する列番号を指定します。
