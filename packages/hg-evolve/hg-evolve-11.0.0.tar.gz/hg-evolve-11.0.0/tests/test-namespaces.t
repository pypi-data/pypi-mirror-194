https://www.mercurial-scm.org/wiki/TopicPlan#sub_branches.2C_namespacing_and_representation

  $ . "$TESTDIR/testlib/topic_setup.sh"

  $ hg init repo
  $ cd repo

  $ hg debug-topic-namespace space-name
  marked working directory as topic namespace: space-name
  $ hg debug-topic-namespaces
  space-name

  $ hg log -r 'wdir()' -T '{topic_namespace}\n'
  space-name

  $ hg log -r 'wdir()' -T '{fqbn}\n'
  default//space-name/

  $ hg branches

  $ hg debug-topic-namespace --clear
  $ hg debug-topic-namespaces
  default

  $ hg debugtopicnamespace --clear nonsense
  abort: cannot use --clear when setting a topic namespace
  [255]

  $ hg branch stable
  marked working directory as branch stable
  (branches are permanent and global, did you want a bookmark?)
  $ hg debug-topic-namespace alice
  marked working directory as topic namespace: alice
  $ hg topic feature
  marked working directory as topic: feature
  $ echo a > a
  $ hg ci -qAm a

  $ hg debug-topic-namespaces
  alice

  $ hg log -r . -T '{rev}: {branch} {topic_namespace} {topic}\n'
  0: stable alice feature

  $ hg log -r . -T '{rev}: {fqbn}\n'
  0: stable//alice/feature

  $ hg branches
  stable//alice/feature          0:69c7dbf6acd1

Updating to a revision with a namespace should activate it

  $ hg up null
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg debug-topic-namespace
  default
  $ hg topics
     feature (1 changesets)
  $ hg up 0
  switching to topic-namespace alice
  switching to topic feature
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg debug-topic-namespace
  alice
  $ hg topics
   * feature (1 changesets)

Updating to a topic namespace is not supported

  $ hg up alice
  abort: unknown revision 'alice'
  [10]

Revsets

  $ nslog() {
  >   hg log -T '{rev}: {topic_namespace}\n' -r "$1"
  > }

  $ nslog 'topicnamespace(:)'
  0: alice
  $ nslog 'topicnamespace(all())'
  0: alice
  $ nslog 'topicnamespace(topicnamespace("alice"))'
  0: alice
  $ nslog 'topicnamespace(wdir())'
  0: alice
  $ nslog 'topicnamespace("re:ice$")'
  0: alice
  $ nslog 'topicnamespace(nonsense)'
  abort: unknown revision 'nonsense'
  [10]

  $ nslog 'topicnamespace("re:nonsense")'
  $ nslog 'topicnamespace("literal:nonsense")'
  abort: topic namespace 'nonsense' does not exist
  [10]

Parsing

  $ hg debugparsefqbn foo/bar//user26/feature -T '[{branch}] <{topic_namespace}> ({topic})\n'
  [foo/bar] <user26> (feature)

no double slashes means it's a named branch
  $ hg debug-parse-fqbn foo/bar
  branch:    foo/bar
  namespace: default
  topic:     

Formatting

  $ hg debugformatfqbn -b branch -n namespace -t topic
  branch//namespace/topic

  $ hg debug-format-fqbn -n namespace
  //namespace/

  $ hg debug-format-fqbn -b foo/bar -n user26 -t feature
  foo/bar//user26/feature

default values

  $ hg debug-format-fqbn -b default -n default -t '' --no-short
  default//default/
  $ hg debug-format-fqbn -b default -n default -t '' --short
  default

  $ hg debug-format-fqbn -b default -n namespace -t '' --no-short
  default//namespace/
  $ hg debug-format-fqbn -b default -n namespace -t '' --short
  default//namespace/

  $ hg debug-format-fqbn -b default -n default -t topic --no-short
  default//default/topic
  $ hg debug-format-fqbn -b default -n default -t topic --short
  default//topic

  $ cd ..
